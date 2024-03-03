import pygame
from API import *
from consts import *


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