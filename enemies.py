from init import *
from weapons import *


class Enemy(pygame.sprite.Sprite):
    ''' Класс, на основе которого создаются персонажи
        path - папка с анимациями персонажа
        speed - скорость в пикселях в секунду
        hp - количество сердец здоровья '''
    def __init__(self, path, bullet, bullet_coords, char_coords=(0, 0), speed=40, hp=5, coords=(0, 0)):
        super().__init__(all_sprites, enemies)
        self.hp = hp
        self.speed = speed / FPS
        self.char_coords = char_coords
        self.bullet = bullet
        self.bullet_coords = bullet_coords
        self.state = 'walk'

        self.walk_frames = self.cut_sheet(load_image(path + '/walk.png'), 4, 4)
        self.attack_frames = self.cut_sheet(load_image(path + '/attack.png'), 4, 4)
        self.cur_frame = 1
        self.cur_rotate = 0
        self.speed_x = 0
        self.speed_y = 0
        self.image = self.walk_frames[self.cur_rotate][self.cur_frame]
        self.rect = self.rect.move(*coords)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(100, 100, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        frames = []
        for j in range(columns):
            frames.append([])
            for i in range(rows):
                frame_location = (self.rect.w * j, self.rect.h * i)
                frames[j].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return frames

    def damage(self, hp):
        self.hp -= hp

    def set_char_coords(self, coords):
        self.char_coords = coords

    def set_speed(self):
        x, y = self.char_coords[0] - self.rect.x, self.char_coords[1] - self.rect.y
        if -50 < x < 20 and -50 < y < 20:
            self.attack()
        elif not x and not y:
            self.speed_x = 0
            self.speed_y = 0
        elif not x:
            self.speed_x = 0
            self.speed_y = self.speed
        elif not y:
            self.speed_y = 0
            self.speed_x = self.speed
        else:
            if max(abs(x), abs(y)) == x:
                self.speed_x = self.speed * (x / abs(x))
                self.speed_y = (y / x) * self.speed * (y / abs(y))
            else:
                self.speed_y = self.speed * (x / abs(x))
                self.speed_x = (x / y) * self.speed * (y / abs(y))

    def attack(self):
        self.speed_x = 0
        self.speed_y = 0
        self.cur_frame = 0
        self.state = 'attack'
        x, y = self.char_coords[0] - self.rect.x, self.char_coords[1] - self.rect.y
        if x >= 0:
            self.cur_rotate = 3
        else:
            self.cur_rotate = 2
        bull = Bullet(self.bullet, damage=0.5, speed=(0, 0), coords=(self.rect.x + self.bullet_coords[0],
                                                                     self.rect.y + self.bullet_coords[1]),
                                                                     good=False, suicide=True)
        bull.cur_rotate = int(self.cur_rotate == 2)

    def update(self, event):
        if self.state == 'attack':
            if self.cur_frame + 1 >= len(self.attack_frames[0]):
                self.state = 'walk'
            self.cur_frame = (self.cur_frame + 1) % len(self.attack_frames[0])
            self.image = self.attack_frames[self.cur_rotate][self.cur_frame]
        elif self.state == 'walk':
            self.set_speed()
            if abs(self.speed_y) > abs(self.speed_x):
                if self.speed_y > 0:
                    self.cur_rotate = 0
                else:
                    self.cur_rotate = 1
            else:
                if self.speed_x > 0:
                    self.cur_rotate = 2
                else:
                    self.cur_rotate = 3
            if 0 <= self.rect.x + self.speed_x <= WINDOW_SIZE[0] - self.rect.width:
                self.rect.x += self.speed_x
            if 0 <= self.rect.y + self.speed_y <= WINDOW_SIZE[1]:
                self.rect.y += self.speed_y
            if self.speed_x or self.speed_y:
                self.cur_frame = (self.cur_frame + 1) % len(self.walk_frames[0])
            self.image = self.walk_frames[self.cur_rotate][self.cur_frame]


class SkeletonSwordman(Enemy):
    def __init__(self, coords=(0, 0)):
        super().__init__(path='images/enemies/skeleton', bullet='images/bullets/24sword_attack.png',
                         bullet_coords=(20, 10), coords=coords, speed=40)