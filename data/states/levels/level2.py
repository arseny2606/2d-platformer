import datetime
import json

import pygame as pg
from ... import setup
from ... import utils
from ... import constants
from ...settings import settings
from ...components.coin import Coin
from ...components.door import Door
from ...components.tile import Tile
from ...components.player import Player
from ...components.camera import Camera


def generate_level(game, level, sprite_group, walls_group, coins_group, finish_group):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('box', x, y, [sprite_group, walls_group])
            elif level[y][x] == "!":
                Tile('trapdoor', x, y, [sprite_group])
            elif level[y][x] == '%':
                Coin([sprite_group, coins_group], utils.load_image("coin.png"), 9, 1, x, y)
            elif level[y][x] == '@':
                new_player = Player(game, x, y, [sprite_group], walls_group, coins_group, finish_group)
            elif level[y][x] == 'F':
                Door(x, y, [sprite_group, finish_group])
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def load_level(filename):
    try:
        filename = "resources/data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        return level_map
    except FileNotFoundError:
        print("Файл не существует")
        exit(0)


class Level2:
    def __init__(self):
        self.screen = setup.screen
        self.bg = utils.load_image("bg.jpg")
        self.bg = pg.transform.scale(self.bg, (constants.width, constants.height))
        self.all_sprites = pg.sprite.Group()
        self.walls_group = pg.sprite.Group()
        self.coins_group = pg.sprite.Group()
        self.finish_group = pg.sprite.Group()
        self.map = load_level("level2.txt")
        self.level = generate_level(self, self.map, self.all_sprites, self.walls_group,
                                    self.coins_group, self.finish_group)
        self.font = pg.font.SysFont("Arial", 25)
        self.coins_text = self.font.render(f"Coins {self.level[0].coins}", True, pg.Color("gold"))
        self.camera = Camera()
        self.loading = True
        self.loader = 10
        self.x = 0
        self.y = 0
        self.is_finished = False

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
        if keys[pg.K_r]:
            self.all_sprites = pg.sprite.Group()
            self.walls_group = pg.sprite.Group()
            self.coins_group = pg.sprite.Group()
            self.map = load_level("level2.txt")
            self.level = generate_level(self, self.map, self.all_sprites, self.walls_group,
                                        self.coins_group, self.finish_group)
            self.camera = Camera()
        if keys[pg.K_ESCAPE]:
            return "back"

    def finish(self):
        self.is_finished = True
        with open("resources/data/leaderboard.json") as f:
            leaderboard = json.load(f)
        leaderboard["users"].append({"name": settings["nickname"],
                                     "time": datetime.datetime.now().strftime("%d.%m.%y в %H:%M"),
                                     "score": self.level[0].coins,
                                     "level": 2})
        with open("resources/data/leaderboard.json", "w") as f:
            json.dump(leaderboard, f, indent=4)
