import os
import sys
import pygame
from random import randint

WINDOW_SIZE = (800, 800)
FPS = 6


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)

all_sprites = pygame.sprite.Group()
characters = pygame.sprite.Group()
enemies = pygame.sprite.Group()


def load_image(name):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image


class Character(pygame.sprite.Sprite):
    ''' Класс, на основе которого создаются персонажи
        path - папка с анимациями персонажа
        speed - скорость в пикселях в секунду
        hp - количество сердец здоровья '''
    def __init__(self, path, weapon, speed=60, hp=5):
        super().__init__(all_sprites)
        characters.add(self)
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
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.weapon.set_coords(self.rect.x + self.rect.width, self.rect.y + 20)
        if self.speed_x or self.speed_y:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[0])
        self.image = self.frames[self.cur_rotate][self.cur_frame]


class Bullet(pygame.sprite.Sprite):
    '''Класс для создания пуль
        path - анимация пули
        speed - скорость по x и y
        coords - начальные координаты
        good - при False калечит персонажей, иначе - врагов'''
    def __init__(self, path, damage=1, speed=(60, 60), coords=(0, 0), good=False):
        super().__init__(all_sprites)
        self.damage = damage
        self.good = good
        self.speed = [speed[0] / FPS, speed[1] / FPS]

        self.frames = self.cut_sheet(load_image(path), int(path.split('/')[-1][0]), int(path.split('/')[-1][1]))
        self.cur_frame = 0
        self.cur_rotate = 0
        self.image = self.frames[self.cur_rotate][self.cur_frame]
        self.rect = self.rect.move(*coords)

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

    def update(self, event):
        if self.good:
            collid = pygame.sprite.spritecollide(self, enemies, dokill=False)
        else:
            collid = pygame.sprite.spritecollide(self, characters, dokill=False)
        if collid:
            collid[0].damage(self.damage)
            self.kill()
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        self.cur_frame = (self.cur_frame + 1) % len(self.frames[0])
        self.image = self.frames[self.cur_rotate][self.cur_frame]


class Weapon(pygame.sprite.Sprite):
    def __init__(self, path, bullet_path, coords=(0, 0), err=20):
        super().__init__(all_sprites)
        self.frames = self.cut_sheet(load_image(path), int(path.split('/')[-1][0]), int(path.split('/')[-1][1]))
        self.err = err
        self.cur_frame = 0
        self.cur_rotate = 0
        self.bullet_path = bullet_path
        self.image = self.frames[self.cur_rotate][self.cur_frame]
        self.rect = self.rect.move(*coords)

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

    def set_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def shoot(self, speed):
        Bullet(self.bullet_path, coords=(self.rect.x + self.rect.width - 5, self.rect.y), speed=speed, good=True)

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == 120:
                self.shoot((60 + randint(-self.err, self.err), 60 + randint(-self.err, self.err)))
        self.cur_frame = (self.cur_frame + 1) % len(self.frames[0])
        self.image = self.frames[self.cur_rotate][self.cur_frame]



char = Character(path='images/characters/witch', weapon=Weapon('images/weapons/13fire_book.png', 'images/bullets/13fire.png'))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        all_sprites.update(event)
    all_sprites.update(event)
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()