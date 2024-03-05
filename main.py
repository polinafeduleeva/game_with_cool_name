import pygame
from random import randint
from init import *
from characters import *
from enemies import *
from weapons import *

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
tile_images = {'floor': load_image('images/fields/floor.png')}
tile_width = tile_height = 96


def make_room(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Pixel(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_room(filename):
    level = make_room(filename)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                Pixel('floor', x, y)

generate_room('rooms/1')
char = Witch(weapon=Weapon('images/weapons/13fire_book.png', 'images/bullets/13fire.png'))
skelet = SkeletonSwordman()

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
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()