import pygame
from init import *
from enemies import *


class Heart(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__(info)
        path = 'images/characters/13hearts.png'
        self.frames = self.cut_sheet(load_image(path),
                                     int(path.split('/')[-1][0]), int(path.split('/')[-1][1]))

        self.image = self.frames[0][0]
        self.rect = self.rect.move(*coords)

    def set_size(self, size):
        if size >= 1:
            self.image = self.frames[0][0]
        elif size == 0.5:
            self.image = self.frames[0][1]
        else:
            self.image = self.frames[0][2]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        frames = []
        for j in range(columns):
            frames.append([])
            for i in range(rows):
                frame_location = (self.rect.w * j, self.rect.h * i)
                frames[j].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return frames


class Info:
    def __init__(self, hp):
        self.hp = hp
        self.hearts = []
        for i in range(hp):
            self.hearts.append(Heart(coords=(i * 35, 0)))

    def set_hp(self, hp):
        self.hp = hp
        for i in range(len(self.hearts)):
            self.hearts[i].set_size(self.hp - i)


class Character(pygame.sprite.Sprite):
    ''' Класс, на основе которого создаются персонажи
        path - папка с анимациями персонажа
        speed - скорость в пикселях в секунду
        hp - количество сердец здоровья '''
    def __init__(self, path, weapon, speed=80, hp=5):
        super().__init__(all_sprites, characters)
        self.weapon = weapon
        self.hp = hp
        self.speed = speed / FPS
        self.count = 0
        self.run_coeff = 1

        self.inf = Info(hp)
        self.frames = []
        self.frames = self.cut_sheet(load_image(path + '/walk.png'), 4, 4)
        self.cur_frame = 1
        self.cur_rotate = 0
        self.speed_x = 0
        self.speed_y = 0
        self.image = self.frames[self.cur_rotate][self.cur_frame]
        self.rect = self.rect.move(200, 200)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
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
        self.inf.set_hp(self.hp)

    def move(self, coords):
        self.rect.x, self.rect.y = coords

    def walk(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if pygame.sprite.spritecollide(self, obstacles, dokill=False):
            self.rect.x -= self.speed_x
            self.rect.y -= self.speed_y

    def update(self, event):
        self.count += 1
        if event.type == pygame.KEYDOWN:
            if event.key == 1073741906:
                self.speed_x = 0
                self.speed_y = -self.speed * self.run_coeff
                self.cur_rotate = 1
            if event.key == 1073741905:
                self.speed_x = 0
                self.speed_y = self.speed * self.run_coeff
                self.cur_rotate = 0
            if event.key == 1073741904:
                self.speed_x = -self.speed * self.run_coeff
                self.speed_y = 0
                self.cur_rotate = 3
            if event.key == 1073741903:
                self.speed_x = self.speed * self.run_coeff
                self.speed_y = 0
                self.cur_rotate = 2
            if event.key == 120:
                collid = []
                for elem in objects:
                    if -100 < elem.rect.x - self.rect.x < 100 and -100 < elem.rect.y - self.rect.y < 100:
                        collid.append(elem)
                if collid:
                    collid[0].interact()
                else:
                    enemy = (10000, 100000)
                    for elem in list(enemies):
                        if abs(elem.rect.x - self.rect.x) + abs(elem.rect.y - self.rect.y) < abs(enemy[0]) + abs(enemy[1]) :
                            enemy = (elem.rect.x - self.rect.x, elem.rect.y - self.rect.y)
                    self.weapon.shoot(enemy)
            if event.key == 122:
                self.run_coeff = 2
                self.speed_x *= 2
                self.speed_y *= 2
        elif event.type == pygame.KEYUP:
            if 1073741903 <= event.key <= 1073741906:
                self.speed_x = 0
                self.speed_y = 0
                self.cur_frame = 0
            if event.key == 122:
                self.speed_x //= self.run_coeff
                self.speed_y //= self.run_coeff
                self.run_coeff = 1
        self.weapon.set_coords(self.rect.x + self.rect.width, self.rect.y + 20)
        if self.count >= FPS // ANIM_FPS:
            self.count = 0
            if self.speed_x or self.speed_y:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames[0])
            self.image = self.frames[self.cur_rotate][self.cur_frame]


class Witch(Character):
    def __init__(self, weapon):
        super().__init__(path='images/characters/witch', weapon=weapon)