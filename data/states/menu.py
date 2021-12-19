import pygame as pg
from .. import setup
from ..components import button
from .. import utils
from .. import constants


class Menu:
    def __init__(self):
        self.screen = setup.screen
        self.buttons = pg.sprite.Group()
        self.bg = utils.load_image("bg.jpg")
        self.bg = pg.transform.scale(self.bg, (constants.width, constants.height))
        rect = self.screen.get_rect()
        rect.y -= 60
        button.Button(self.buttons, "Story mode", rect)
        rect.y += 60
        button.Button(self.buttons, "Infinite mode", rect)
        rect.y += 60
        button.Button(self.buttons, "Options", rect)
        self.x = 0
        self.y = 0

    def render(self):
        self.screen.blit(self.bg, (0, 0))
        self.buttons.draw(self.screen)
        self.buttons.update()


class Options:
    def __init__(self):
        pass
