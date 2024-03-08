import pygame
from init import *
from enemies import *


class Heart(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__(all_sprites)
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
    def __init__(self, path, weapon, speed=60, hp=5):
        super().__init__(all_sprites, characters)
        self.weapon = weapon
        self.hp = hp
        self.speed = speed / FPS

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

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == 1073741906:
                self.speed_x = 0
                self.speed_y = -self.speed
                self.cur_rotate = 1
            if event.key == 1073741905:
                self.speed_x = 0
                self.speed_y = self.speed
                self.cur_rotate = 0
            if event.key == 1073741904:
                self.speed_x = -self.speed
                self.speed_y = 0
                self.cur_rotate = 3
            if event.key == 1073741903:
                self.speed_x = self.speed
                self.speed_y = 0
                self.cur_rotate = 2
            if event.key == 120:
                enemy = (10000, 100000)
                for elem in list(enemies):
                    if abs(elem.rect.x - self.rect.x) + abs(elem.rect.y - self.rect.y) < abs(enemy[0]) + abs(enemy[1]) :
                        enemy = (elem.rect.x - self.rect.x, elem.rect.y - self.rect.y)
                self.weapon.shoot(enemy)
            # для теста
            if event.key == 122:
                skelet = SkeletonSwordman()
        elif event.type == pygame.KEYUP:
            if 1073741903 <= event.key <= 1073741906:
                self.speed_x = 0
                self.speed_y = 0
                self.cur_frame = 1
        if 0 <= self.rect.x + self.speed_x <= WINDOW_SIZE[0] - self.rect.width:
            self.rect.x += self.speed_x
        if 0 <= self.rect.y + self.speed_y <= WINDOW_SIZE[1]:
            self.rect.y += self.speed_y
        self.weapon.set_coords(self.rect.x + self.rect.width, self.rect.y + 20)
        if self.speed_x or self.speed_y:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[0])
        self.image = self.frames[self.cur_rotate][self.cur_frame]


class Witch(Character):
    def __init__(self, weapon):
        super().__init__(path='images/characters/witch', weapon=weapon)