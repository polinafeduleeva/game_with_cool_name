import pygame
from API import *
from consts import *


class Enemy(pygame.sprite.Sprite):
    ''' Класс, на основе которого создаются персонажи
        path - папка с анимациями персонажа
        speed - скорость в пикселях в секунду
        hp - количество сердец здоровья '''
    def __init__(self, path, char_coords=(0, 0), speed=40, hp=5, coords=(0, 0)):
        super().__init__(all_sprites, enemies)
        self.hp = hp
        self.speed = speed / FPS
        self.char_coords = char_coords

        self.frames = []
        self.frames = self.cut_sheet(load_image(path + '/walk.png'), 4, 4)
        self.cur_frame = 1
        self.cur_rotate = 0
        self.speed_x = 0
        self.speed_y = 0
        self.image = self.frames[self.cur_rotate][self.cur_frame]
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
        if not x and not y:
            self.speed_x = 0
            self.speed_y = 0
        elif not x:
            self.speed_x = 0
            self.speed_y = self.speed
        elif not y:
            self.speed_y = 0
            self.speed_x = self.speed
        else:
            if max(x, y) == x:
                self.speed_x = self.speed * (x / abs(x))
                self.speed_y = (y / x) * self.speed * (y / abs(y))
            else:
                self.speed_y = self.speed * (x / abs(x))
                self.speed_x = (x / y) * self.speed * (y / abs(y))

    def update(self, event):
        self.set_speed()
        if 0 <= self.rect.x + self.speed_x <= WINDOW_SIZE[0] - self.rect.width:
            self.rect.x += self.speed_x
        if 0 <= self.rect.y + self.speed_y <= WINDOW_SIZE[1]:
            self.rect.y += self.speed_y
        if self.speed_x or self.speed_y:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[0])
        self.image = self.frames[self.cur_rotate][self.cur_frame]