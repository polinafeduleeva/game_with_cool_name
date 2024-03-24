from init import *


class Object(pygame.sprite.Sprite):
    def __init__(self, path, coords=(200, 200), is_new=True):
        super().__init__(all_sprites, objects, obstacles)
        self.count = 0
        self.cur_frame = 0
        self.cur_rotate = 0
        self.can_interact = True
        self.do_interact = False
        self.is_new = is_new
        self.frames = self.cut_sheet(load_image(path), int(path.split('/')[-1][0]), int(path.split('/')[-1][1]))
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

    def interact(self):
        self.do_interact = True

    def update(self, event):
        self.image = self.frames[self.cur_rotate][self.cur_frame]


class Chest(Object):
    def __init__(self, coords=(200, 200), is_new=True):
        super().__init__('images/objects/14rock_chest.png', coords, is_new)
        if not is_new:
            self.cur_frame = len(self.frames[0]) - 1

    def update(self, event):
        if self.do_interact:
            if self.cur_frame == len(self.frames[0]) - 1:
                self.do_interact = False
            else:
                self.cur_frame += 1
        super().update(event)
