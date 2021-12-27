import pygame as pg
from .. import utils
from .. import constants
from ..settings import settings

player_image = utils.load_image('mar.png')


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, sprite_groups, walls_group):
        super().__init__()
        for i in sprite_groups:
            i.add(self)
        self.image = player_image
        self.rect = self.image.get_rect().move(constants.tile_width * pos_x + 15,
                                               constants.tile_height * pos_y + 5 + constants.height / 2)
        self.walls_group = walls_group
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

    def move(self, keys):
        dx = 0
        dy = 0

        if keys[pg.K_UP] and not self.jumped and not self.in_air:
            self.vel_y = -20
            self.jumped = True
        if not keys[pg.K_UP]:
            self.jumped = False
        if keys[pg.K_LEFT]:
            dx -= 5
            self.direction = -1
        if keys[pg.K_RIGHT]:
            dx += 5
            self.direction = 1

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        self.in_air = True
        for tile in self.walls_group:
            tile = tile.rect
            if tile.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile.bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile.top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        self.rect.x += dx
        self.rect.y += dy
