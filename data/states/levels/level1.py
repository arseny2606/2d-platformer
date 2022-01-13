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


class Level1:
    def __init__(self):
        self.screen = setup.screen
        self.bg = utils.load_image("bg.jpg")
        self.bg = pg.transform.scale(self.bg, (constants.width, constants.height))
        self.all_sprites = pg.sprite.Group()
        self.walls_group = pg.sprite.Group()
        self.coins_group = pg.sprite.Group()
        self.finish_group = pg.sprite.Group()
        self.map = load_level("level1.txt")
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
        pg.mixer.music.stop()
        pg.mixer.music.load("resources/sounds/game.mp3")
        pg.mixer.music.play(-1)

    def update(self, keys, clicks):
        if self.is_finished:
            pg.mixer.music.stop()
            pg.mixer.music.load("resources/sounds/menu.mp3")
            pg.mixer.music.play(-1)
            self.screen.blit(utils.load_image("bg.jpg"), (0, 0))
            font = pg.font.SysFont("Arial", 60)
            text = font.render("You won!", True,
                               pg.Color("red"))
            self.screen.blit(text,
                             (text.get_rect(center=(constants.width // 2, constants.height // 3))))
            text = font.render(f"Your score is {self.level[0].coins} coins", True,
                               pg.Color("gold"))
            self.screen.blit(text,
                             (text.get_rect(
                                 center=(constants.width // 2, constants.height // 3 * 2))))
            pg.display.flip()
            pg.time.wait(4000)
            return "back"
        else:
            self.screen.blit(self.bg, (0, 0))
            if self.loading:
                pg.draw.rect(self.screen, "red", [100, constants.height // 2 - 5, self.loader, 10])
                self.loader += 10
                if self.loader >= constants.width - 100:
                    self.loading = False
                return
            self.level[0].move(keys)
            self.all_sprites.draw(self.screen)
            self.all_sprites.update()
            self.coins_text = self.font.render(f"Coins {self.level[0].coins}", True, pg.Color("gold"))
            self.screen.blit(self.coins_text, (constants.width - 100, 0))
            self.camera.update(self.level[0])
            for sprite in self.all_sprites:
                self.camera.apply(sprite)
            if keys[pg.K_r]:
                self.all_sprites = pg.sprite.Group()
                self.walls_group = pg.sprite.Group()
                self.coins_group = pg.sprite.Group()
                self.finish_group = pg.sprite.Group()
                self.map = load_level("level1.txt")
                self.level = generate_level(self, self.map, self.all_sprites, self.walls_group,
                                            self.coins_group, self.finish_group)
                self.camera = Camera()
            if keys[pg.K_ESCAPE]:
                pg.mixer.music.stop()
                pg.mixer.music.load("resources/sounds/menu.mp3")
                pg.mixer.music.play(-1)
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
