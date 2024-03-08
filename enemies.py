from init import *
from weapons import *
from time import time
from random import randint


class Enemy(pygame.sprite.Sprite):
    ''' Класс, на основе которого создаются персонажи
        path - папка с анимациями персонажа
        speed - скорость в пикселях в секунду
        hp - количество сердец здоровья '''
    def __init__(self, path, bullet, bullet_coords, char_coords=(0, 0), speed=40, hp=5, coords=(0, 0), attack_range=20,
                 cd=2):
        super().__init__(all_sprites, enemies)
        self.hp = hp
        self.speed = speed / FPS
        self.char_coords = char_coords
        self.bullet = bullet
        self.bullet_coords = bullet_coords
        self.attack_range = attack_range
        self.cd = cd
        self.timer = time()
        self.state = 'walk'

        self.walk_frames = self.cut_sheet(load_image(path + '/walk.png'), 4, 4)
        self.attack_frames = self.cut_sheet(load_image(path + '/attack.png'), 4, 4)
        self.dead_frames = self.cut_sheet(load_image(path + '/dead.png'), 4, 4)
        self.cur_frame = 1
        self.cur_rotate = 0
        self.speed_x = 0
        self.speed_y = 0
        self.image = self.walk_frames[self.cur_rotate][self.cur_frame]
        self.rect = self.rect.move(*coords)
        self.mask = pygame.mask.from_surface(self.image)

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
        if self.hp <= 0:
            self.state = 'dead'
            self.cur_frame = 0

    def set_char_coords(self, coords):
        if time() - self.timer < self.cd:
            self.char_coords = (coords[0] + randint(-60, 60), coords[1] + randint(-60, 60))
        else:
            self.char_coords = coords

    def set_speed(self):
        x, y = self.char_coords[0] - self.rect.x, self.char_coords[1] - self.rect.y
        if -self.attack_range - CHAR_SIZE[0] < x < self.attack_range + CHAR_SIZE[0] and -CHAR_SIZE[1] < y < 0:
            if time() - self.timer >= self.cd:
                self.attack()
        else:
            if x or y:
                if max(abs(x), abs(y)) == abs(x):
                    self.speed_x = self.speed
                    self.speed_y = abs((y / x) * self.speed)
                else:
                    self.speed_y = self.speed
                    self.speed_x = abs((x / y) * self.speed)
                if x < 0:
                    self.speed_x *= -1
                if y < 0:
                    self.speed_y *= -1

    def attack(self):
        self.timer = time()
        self.speed_x = 0
        self.speed_y = 0
        self.cur_frame = 0
        self.state = 'attack'

    def update(self, event):
        if self.state == 'dead':
            if self.cur_frame + 1 >= len(self.dead_frames[0]):
                self.kill()
            self.cur_frame = self.cur_frame + 1
            self.image = self.dead_frames[self.cur_rotate][min(self.cur_frame, 3)]
        elif self.state == 'attack':
            if self.cur_frame + 1 >= len(self.attack_frames[0]):
                self.state = 'walk'
                self.speed_x = randint(-int(self.speed), int(self.speed))
                self.speed_y = randint(-int(self.speed), int(self.speed))
            self.cur_frame = (self.cur_frame + 1) % len(self.attack_frames[0])
            self.image = self.attack_frames[self.cur_rotate][self.cur_frame]
        elif self.state == 'walk':
            self.set_speed()
            if self.speed_y or self.speed_x:
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
            self.mask = pygame.mask.from_surface(self.image)


class SkeletonSwordman(Enemy):
    def __init__(self, coords=(0, 0)):
        super().__init__(path='images/enemies/skeleton', bullet='images/bullets/24sword_attack.png', cd=4,
                         bullet_coords=(10, 10), coords=coords, speed=40)

    def attack(self):
        super().attack()
        if self.char_coords[0] + (CHAR_SIZE[0] / 2) <= self.rect.x:
            self.cur_rotate = 3
            coords = (self.rect.x + self.bullet_coords[0], self.rect.y + self.bullet_coords[1])
        else:
            self.cur_rotate = 2
            coords = (self.rect.x + self.bullet_coords[0] + self.rect.width - 10, self.rect.y + self.bullet_coords[1])
        bull = Bullet(self.bullet, damage=0.5, speed=(0, 0), coords=coords, good=False, suicide=True)
        bull.cur_rotate = int(self.cur_rotate == 3)
