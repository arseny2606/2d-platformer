import pygame as pg
from .. import utils
from .. import constants


player_image = utils.load_image('mar.png')


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, sprite_groups, walls_group):
        super().__init__()
        for i in sprite_groups:
            i.add(self)
        self.image = player_image
        self.rect = self.image.get_rect().move(constants.tile_width * pos_x + 15, constants.tile_height * pos_y + 5 + constants.height / 2)
        self.walls_group = walls_group

    def move(self, keys):
        if keys[pg.K_RIGHT]:
            self.rect = self.rect.move(1, 0)
            if pg.sprite.spritecollideany(self, self.walls_group):
                self.rect = self.rect.move(-1, 0)
        elif keys[pg.K_LEFT]:
            self.rect = self.rect.move(-1, 0)
            if pg.sprite.spritecollideany(self, self.walls_group):
                self.rect = self.rect.move(1, 0)
        elif keys[pg.K_UP]:
            self.rect = self.rect.move(0, -1)
            if pg.sprite.spritecollideany(self, self.walls_group):
                self.rect = self.rect.move(0, 1)
        elif keys[pg.K_DOWN]:
            self.rect = self.rect.move(0, 1)
            if pg.sprite.spritecollideany(self, self.walls_group):
                self.rect = self.rect.move(0, -1)
