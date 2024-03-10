import os
import sys
import pygame

WINDOW_SIZE = (780, 690)
CHAR_SIZE = (50, 150)
FPS = 6

all_sprites = pygame.sprite.LayeredUpdates()
info = pygame.sprite.Group()
characters = pygame.sprite.Group()
enemies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
teleports = pygame.sprite.Group()


def load_image(name):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image


underground_images = {'floor': [load_image('images/fields/underground/floor1.png'),
                                load_image('images/fields/underground/floor2.png'),
                                load_image('images/fields/underground/floor3.png'),
                                load_image('images/fields/underground/floor4.png'),
                                load_image('images/fields/underground/floor5.png')],
                       'wall': [load_image('images/fields/underground/wall1.png'),
                                load_image('images/fields/underground/wall2.png')],
                       'door': [load_image('images/fields/underground/wall1.png')],
                       'door_open': [load_image('images/fields/underground/open_door.png')]}
