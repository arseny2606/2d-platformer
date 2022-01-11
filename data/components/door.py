import pygame as pg
from .. import utils
from .. import constants

door_image = utils.load_image("door.png")


class Door(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, sprite_groups):
        super().__init__()
        for i in sprite_groups:
            i.add(self)
        self.image = door_image
        self.rect = self.image.get_rect().move(constants.tile_width * pos_x, constants.tile_height * pos_y + constants.height / 2)
