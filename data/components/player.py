import pygame as pg
from .. import utils
from .. import constants
from ..settings import settings
import time


player_image = utils.load_image('player.png')
player_image = pg.transform.scale(player_image, (1792, 64))


class Player(pg.sprite.Sprite):
    def __init__(self, game, pos_x, pos_y, sprite_groups, walls_group, coins_group, finish_group):
        super().__init__()
        for i in sprite_groups:
            i.add(self)
        self.frames = []
        self.columns = 28
        self.idle_frames = self.cut_sheet(player_image, 0, 9, False)
        self.walk_frames = self.cut_sheet(player_image, 9, 15, False)
        self.backward_walk_frames = self.cut_sheet(player_image, 9, 15, True)
        self.frames = self.idle_frames
        self.cur_frame = 0
        self.start_frame = time.time()
        self.noi = 9
        self.frames_per_second = 5
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(constants.tile_width * pos_x + 15,
                                               constants.tile_height * pos_y + 5 + constants.height / 2)
        self.game = game
        self.walls_group = walls_group
        self.coins_group = coins_group
        self.finish_group = finish_group
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
        self.dx = 0
        self.dy = 0
        self.old_time = 0.0
        self.time = pg.time.get_ticks()
        self.coins = 0

    def cut_sheet(self, sheet, start, end, backward):
        self.rect = pg.Rect(0, 0, sheet.get_width() // self.columns,
                            sheet.get_height() // 1)
        frames = []
        for j in range(1):
            for i in range(start, end):
                frame_location = (self.rect.w * i, self.rect.h * j)
                temp = sheet.subsurface(pg.Rect(
                    frame_location, self.rect.size))
                temp = temp.subsurface(pg.Rect(12, 12, 28, 40))
                if backward:
                    temp = pg.transform.flip(temp, True, False)
                frames.append(temp)
        return frames

    def move(self, keys):
        self.time = pg.time.get_ticks()
        self.dy = 0
        if keys[pg.K_SPACE] and self.old_time + 60 < self.time:
            settings["debug"] = not settings["debug"]
        if keys[pg.K_UP] and (not self.jumped and not self.in_air or settings["debug"]):
            self.vel_y = -10
            self.jumped = True
        if not keys[pg.K_UP]:
            self.jumped = False
        if keys[pg.K_LEFT]:
            self.dx -= 0.5
            if self.dx < -5 and not settings["debug"]:
                self.dx = -5
            self.direction = -1
        if keys[pg.K_RIGHT]:
            self.dx += 0.5
            if self.dx > 5 and not settings["debug"]:
                self.dx = 5
            self.direction = 1
        self.vel_y += 0.5
        if self.vel_y > 5:
            self.vel_y = 5
        self.dy += self.vel_y
        self.in_air = True
        for tile in self.walls_group:
            tile = tile.rect
            if tile.colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height) and not settings["debug"]:
                self.dx = 0
            if tile.colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height) and not settings["debug"]:
                if self.vel_y < 0:
                    self.dy = tile.bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    self.dy = tile.top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        for tile in self.coins_group:
            tile_rect = tile.rect
            if tile_rect.colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height) and not settings["debug"]:
                tile.kill()
                self.coins += 1

        for tile in self.finish_group:
            tile_rect = tile.rect
            if tile_rect.colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height) and not settings["debug"]:
                self.game.finish()

        self.rect.x += self.dx
        self.rect.y += self.dy

        self.cur_frame = int((time.time() - self.start_frame) * self.frames_per_second % self.noi)
        self.image = self.frames[self.cur_frame]

    def update(self):
        if self.dx > 0:
            self.noi = 6
            self.frames = self.walk_frames
        elif self.dx < 0:
            self.noi = 6
            self.frames = self.backward_walk_frames
        else:
            self.noi = 9
            self.frames = self.idle_frames


class InfinitePlayer(Player):
    def __init__(self, game, pos_x, pos_y, sprite_groups, walls_group, coins_group, finish_group):
        super().__init__(game, pos_x, pos_y, sprite_groups, walls_group, coins_group, finish_group)

    def move(self, keys):
        self.time = pg.time.get_ticks()
        self.dy = 0
        if keys[pg.K_SPACE] and self.old_time + 60 < self.time:
            settings["debug"] = not settings["debug"]
        if keys[pg.K_UP] and (not self.jumped and not self.in_air or settings["debug"]):
            self.vel_y = -10
            self.jumped = True
        if not keys[pg.K_UP]:
            self.jumped = False
        self.vel_y += 0.5
        if self.vel_y > 5:
            self.vel_y = 5
        self.dy += self.vel_y
        self.in_air = True
        for tile in self.walls_group:
            tile = tile.rect
            if tile.colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height) and not settings["debug"]:
                self.dx = 0
            if tile.colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height) and not settings["debug"]:
                if self.vel_y < 0:
                    self.dy = tile.bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    self.dy = tile.top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        for tile in self.coins_group:
            tile_rect = tile.rect
            if tile_rect.colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height) and not settings[
                "debug"]:
                tile.kill()
                self.coins += 1

        for tile in self.finish_group:
            tile_rect = tile.rect
            if tile_rect.colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height) and not settings[
                "debug"]:
                self.game.finish()

        self.rect.x += self.dx
        self.rect.y += self.dy

        self.cur_frame = int((time.time() - self.start_frame) * self.frames_per_second % self.noi)
        self.image = self.frames[self.cur_frame]

    def update(self):
        self.noi = 6
        self.frames = self.walk_frames
