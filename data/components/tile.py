import pygame as pg
from .. import utils
from .. import constants

tile_images = {
    'box': utils.load_image('box.png'),
    'trapdoor': utils.load_image('trapdoor.png'),
    'danger': utils.load_image('danger.png')
}


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, sprite_groups):
        super().__init__()
        for i in sprite_groups:
            i.add(self)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(constants.tile_width * pos_x, constants.tile_height * pos_y + constants.height / 2)
        self.dx = 0
        self.direction = 0


class DangerTile(Tile):
    def __init__(self, tile_type, pos_x, pos_y, sprite_groups):
        super().__init__(tile_type, pos_x, pos_y, sprite_groups)
