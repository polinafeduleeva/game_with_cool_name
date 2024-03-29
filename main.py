from random import choice
from init import *
from characters import *
from enemies import *
from weapons import *
from objects import *


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
tile_width = tile_height = 30
underground_enemies = [SkeletonSwordman, Slime]
level_map = {1: {'map': 'rooms/start_room', 'type': 'start', 'obj': [], 'new': True, 1: None, 2: 2, 3: None, 4: None},
             2: {'map': 'rooms/battlefields/1', 'type': 'battlefield', 'obj': [], 'new': True, 1: None, 2: 3, 3: None, 4: 1},
             3: {'map': 'rooms/battlefields/2', 'type': 'event', 'obj': [], 'new': True, 1: None, 2: None, 3: None, 4: 2}}


def make_room(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Pixel(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tp=None):
        super().__init__(all_sprites)
        self.image = choice(underground_images[tile_type])
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.type = tile_type
        self.tp = tp
        if self.type == 'wall' or self.type == 'door':
            obstacles.add(self)

    def open(self):
        if self.type == 'door':
            self.type = 'door_open'
            obstacles.remove(self)
            teleports.add(self)
            self.image = underground_images['door_open'][0]

    def close(self):
        if self.type == 'door_open':
            self.type = 'door'
            self.image = underground_images['door'][0]
            obstacles.add(self)
            teleports.remove(self)

    def __repr__(self):
        return self.type


class Room:
    def __init__(self, name, last_room):
        self.name = name
        self.char_coords = (0, 0)
        self.objects = []
        if last_room in level_map:
            self.last_room = [i for i in range(1, 5) if level_map[last_room][i] == name][0]
        else:
            self.last_room = 0
        self.field = self.generate_room(level_map[name]['map'])
        if level_map[name]['type'] == 'battlefield' and level_map[name]['new']:
            for i in range(5):
                choice(underground_enemies)(coords=(randint(300, len(self.field[0]) * tile_width - 300),
                                                    randint(300, len(self.field) * tile_height) - 300))
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                all_sprites.move_to_back(self.field[y][x])

    def generate_room(self, filename):
        level = make_room(filename)
        field = []
        for y in range(len(level)):
            field.append([])
            for x in range(len(level[y])):
                if level[y][x] == '*':
                    field[y].append(Pixel('floor', x, y))
                elif level[y][x] == '$':
                    field[y].append(Pixel('floor', x, y))
                    self.objects.append(Chest(((x - 1) * tile_width, (y - 1) * tile_height)))
                elif level[y][x] == 'X':
                    field[y].append(Pixel('wall', x, y))
                elif level[y][x] == 'C':
                    field[y].append(Pixel('floor', x, y))
                    if ((self.last_room == 1 and y < len(level) // 2)
                            or (self.last_room == 4 and x > len(level[y]) // 2)
                            or (self.last_room == 3 and y > len(level) // 2)
                            or (self.last_room == 2 and x < len(level[y]) // 2)) or self.last_room == 0:
                        self.char_coords = (x * tile_width, y * tile_height)
                elif level[y][x] == '1' or level[y][x] == '2' or level[y][x] == '3' or level[y][x] == '4':
                    field[y].append(Pixel('door', x, y, level_map[self.name][int(level[y][x])]))
        return field

    def open(self):
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                self.field[y][x].open()

    def close(self):
        for y in range(len(self.field)):
            for x in range(len(self.field[0])):
                self.field[y][x].close()

    def remove(self):
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                self.field[y][x].kill()
        for elem in self.objects:
            elem.kill()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WINDOW_SIZE[0] // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - WINDOW_SIZE[1] // 2)


room = Room(1, 0)
camera = Camera()
char = Witch(weapon=FireBook())

clock = pygame.time.Clock()
running = True
do_loop = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        do_loop = False
        all_sprites.update(event)
        info.update(event)
    screen.fill((0, 0, 0))
    if len(list(enemies)) == 0:
        room.open()
    if do_loop:
        all_sprites.update(event)
    do_loop = True
    for elem in enemies:
        elem.set_char_coords((char.rect.x, char.rect.y))

    collid = pygame.sprite.spritecollide(char, teleports, dokill=False)
    if collid:
        level_map[room.name]['new'] = False
        name = room.name
        room.remove()
        room = Room(collid[0].tp, name)
        char.move(room.char_coords)
    for sprite in all_sprites:
        camera.apply(sprite)
    camera.update(char)
    char.walk()
    all_sprites.draw(screen)
    info.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()