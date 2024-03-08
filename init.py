import os
import sys
import pygame

WINDOW_SIZE = (780, 690)
CHAR_SIZE = (50, 150)
FPS = 6
all_sprites = pygame.sprite.Group()
characters = pygame.sprite.Group()
enemies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()


def load_image(name):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image