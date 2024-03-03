import os
import sys
import pygame

all_sprites = pygame.sprite.Group()
characters = pygame.sprite.Group()
enemies = pygame.sprite.Group()


def load_image(name):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image
