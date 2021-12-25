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
        self.speed_x = 0
        self.speed_y = 0
        self.jump_start = 0

    def get_collisions(self, group):
        return pg.sprite.spritecollideany(self, group)

    def move(self, keys):
        if not self.speed_y:
            if keys[pg.K_RIGHT]:
                self.speed_x += 1
                if self.speed_x > 5:
                    self.speed_x = 5
            elif keys[pg.K_LEFT]:
                self.speed_x -= 1
                if self.speed_x < -5:
                    self.speed_x = -5
            elif keys[pg.K_UP]:
                self.speed_y = -5
                self.jump_start = pg.time.get_ticks()
        if not self.speed_x and not self.speed_y and self.get_collisions(self.walls_group):
            collision_sprite = self.get_collisions(self.walls_group)
            if collision_sprite.rect.x <= self.rect.x:
                self.speed_x = 5
            else:
                self.speed_x = -5
            if collision_sprite.rect.y <= self.rect.y:
                self.speed_y = 5
            else:
                self.speed_y = -5
            self.rect = self.rect.move(self.speed_x, self.speed_y)
            self.speed_x = 0
            self.speed_y = 0
        else:
            self.rect = self.rect.move(self.speed_x, self.speed_y)
            if self.get_collisions(self.walls_group):
                self.rect.move(-self.speed_x, -self.speed_y)
                self.speed_x = 0
                self.speed_y = 0
            if self.jump_start and (pg.time.get_ticks() - self.jump_start) / 1000 >= 0.5:
                self.speed_y = 3
                self.jump_start = 0
