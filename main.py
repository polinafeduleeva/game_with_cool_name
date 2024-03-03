import pygame
from random import randint
from consts import *
from characters import *
from enemies import *

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)


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


char = Witch(weapon=Weapon('images/weapons/13fire_book.png', 'images/bullets/13fire.png'))
skelet = Enemy(path='images/enemies/skeleton')

clock = pygame.time.Clock()
running = True
do_loop = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        do_loop = False
        all_sprites.update(event)
    if do_loop:
        all_sprites.update(event)
    do_loop = True
    for elem in enemies:
        elem.set_char_coords((char.rect.x, char.rect.y))
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()