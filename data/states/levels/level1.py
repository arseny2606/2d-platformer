import pygame as pg
from ... import setup
from ... import utils
from ... import constants
from ...components.tile import Tile
from ...components.player import Player


def generate_level(level, sprite_group, walls_group):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('box', x, y, [sprite_group, walls_group])
            elif level[y][x] == '@':
                new_player = Player(x, y, [sprite_group], walls_group)
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
        self.map = load_level("level1.txt")
        self.level = generate_level(self.map, self.all_sprites, self.walls_group)
        self.x = 0
        self.y = 0

    def update(self, keys, clicks):
        self.screen.blit(self.bg, (0, 0))
        self.level[0].move(keys)
        self.all_sprites.draw(self.screen)
        if keys[pg.K_ESCAPE]:
            return "back"
