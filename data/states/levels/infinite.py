import datetime
import json
import random

import pygame as pg
from ... import setup
from ... import utils
from ... import constants
from ...settings import settings
from ...components.coin import Coin
from ...components.tile import Tile, DangerTile
from ...components.player import InfinitePlayer
from ...components.camera import Camera


def load_level(filename):
    try:
        filename = "resources/data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        return level_map
    except FileNotFoundError:
        print("Файл не существует")
        exit(0)


class InfiniteLevel:
    def __init__(self):
        self.screen = setup.screen
        self.bg = utils.load_image("bg.jpg")
        self.bg = pg.transform.scale(self.bg, (constants.width, constants.height))
        self.all_sprites = pg.sprite.Group()
        self.walls_group = pg.sprite.Group()
        self.coins_group = pg.sprite.Group()
        self.finish_group = pg.sprite.Group()
        self.walls_segment = []
        self.danger_segment = []
        self.coins_segment = []
        self.map = load_level("infinite_start.txt")
        self.level = self.generate_level(self, self.map, self.all_sprites, self.walls_group,
                                         self.coins_group, self.finish_group, None, 0)
        for i in range(2):
            self.map = load_level(f"infinite_seg{random.randint(1, 6)}.txt")
            self.level = self.generate_level(self, self.map, self.all_sprites, self.walls_group,
                                             self.coins_group, self.finish_group, self.level[0], self.level[1])
        self.font = pg.font.SysFont("Arial", 25)
        self.coins_text = self.font.render(f"Coins {self.level[0].coins}", True, pg.Color("gold"))
        self.camera = Camera()
        self.loading = True
        self.loader = 10
        self.x = 0
        self.y = 0
        self.is_finished = False
        self.check = True

    def update(self, keys, clicks):
        if self.is_finished:
            return "back"
        self.screen.blit(self.bg, (0, 0))
        if self.loading:
            pg.draw.rect(self.screen, "red", [100, constants.height // 2 - 5, self.loader, 10])
            self.loader += 10
            if self.loader >= 1080:
                self.loading = False
            return
        self.level[0].move(keys)
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
        self.coins_text = self.font.render(f"Coins {self.level[0].coins}", True, pg.Color("gold"))
        self.screen.blit(self.coins_text, (1150, 0))
        self.camera.update(self.level[0])
        for sprite in self.all_sprites:
            self.camera.apply(sprite)
        self.level[0].update()
        if self.walls_group.sprites()[0].rect.x <= -500 and self.check:
            self.check = False
            for i in range(2):
                for j in self.walls_segment[i]:
                    self.walls_group.remove(j)
                    self.all_sprites.remove(j)
            last_x = self.walls_group.sprites()[-1].rect.x
            self.coins_group = pg.sprite.Group()
            self.finish_group = pg.sprite.Group()
            self.level[0].walls_group = self.walls_group
            self.level[0].coins_group = self.coins_group
            self.level[0].finish_group = self.finish_group
            for i in range(5):
                self.map = load_level(f"infinite_seg{random.randint(1, 6)}.txt")
                self.level = self.generate_level_next(self, self.map, self.all_sprites, self.walls_group,
                                                      self.coins_group, self.finish_group, self.level[0], self.level[1], last_x)

        if keys[pg.K_ESCAPE]:
            return "back"

    def finish(self):
        self.is_finished = True
        with open("resources/data/leaderboard.json") as f:
            leaderboard = json.load(f)
        leaderboard["users"].append({"name": settings["nickname"],
                                     "time": datetime.datetime.now().strftime("%d.%m.%y в %H:%M"),
                                     "score": self.level[0].coins,
                                     "level": 1})
        with open("resources/data/leaderboard.json", "w") as f:
            json.dump(leaderboard, f, indent=4)

    def generate_level(self, game, level, sprite_group, walls_group, coins_group, finish_group, player, old_x):
        x, y = 0, 0
        temp_walls = []
        temp_danger = []
        temp_coins = []
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '#':
                    f = Tile('box', x + old_x, y, [sprite_group, walls_group])
                    temp_walls.append(f)
                if level[y][x] == '!':
                    f = DangerTile('danger', x + old_x, y, [sprite_group, finish_group])
                    temp_danger.append(f)
                elif level[y][x] == '%':
                    f = Coin([sprite_group, coins_group], utils.load_image("coin.png"), 9, 1, x + old_x, y)
                    temp_coins.append(f)
                elif level[y][x] == '@':
                    player = InfinitePlayer(game, x, y, [sprite_group], walls_group, coins_group,
                                            finish_group)
        # вернем игрока, а также размер поля в клетках
        self.walls_segment.append(temp_walls)
        self.danger_segment.append(temp_danger)
        self.coins_segment.append(temp_coins)
        return player, x + old_x, y

    def generate_level_next(self, game, level, sprite_group, walls_group, coins_group, finish_group, player, old_x, last_x):
        x, y = 0, 0
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '#':
                    f = Tile('box', x + old_x, y, [sprite_group, walls_group])
                if level[y][x] == '!':
                    f = DangerTile('danger', x + old_x, y, [sprite_group, finish_group])
                elif level[y][x] == '%':
                    f = Coin([sprite_group, coins_group], utils.load_image("coin.png"), 9, 1, x + old_x, y)
                f.rect.y -= 230
        # вернем игрока, а также размер поля в клетках
        return player, x + old_x, y
