import pygame as pg
from .. import constants
import time


class Coin(pg.sprite.Sprite):
    def __init__(self, sprite_groups, sheet, columns, rows, x, y):
        super().__init__()
        for i in sprite_groups:
            i.add(self)
        self.frames = []
        sheet = pg.transform.scale(sheet, (450, 50))
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.start_frame = time.time()
        self.noi = 9
        self.frames_per_second = 9
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(constants.tile_width * x, constants.tile_height * y + constants.height / 2)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pg.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pg.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = int((time.time() - self.start_frame) * self.frames_per_second % self.noi)
        self.image = self.frames[self.cur_frame]
