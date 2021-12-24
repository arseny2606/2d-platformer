import pygame as pg
from .. import setup
from ..components import button, checkbox
from .. import utils
from .. import constants
from ..settings import settings


class Menu:
    def __init__(self):
        self.states = {"Story mode": "story",
                       "Infinite mode": "infinite",
                       "Options": "options",
                       "Exit": "exit"}
        self.screen = setup.screen
        self.buttons = pg.sprite.Group()
        self.bg = utils.load_image("bg.jpg")
        self.bg = pg.transform.scale(self.bg, (constants.width, constants.height))
        rect = self.screen.get_rect()
        rect.y -= 90
        button.Button(self.buttons, "Story mode", rect)
        rect.y += 60
        button.Button(self.buttons, "Infinite mode", rect)
        rect.y += 60
        button.Button(self.buttons, "Options", rect)
        rect.y += 60
        button.Button(self.buttons, "Exit", rect)
        self.x = 0
        self.y = 0

    def update(self, keys, clicks):
        self.screen.blit(self.bg, (0, 0))
        self.buttons.draw(self.screen)
        for i in self.buttons:
            state = i.update(clicks)
            if state:
                return self.states[state]
        return False


class Options:
    def __init__(self):
        self.states = {"Show FPS": "show_fps"}
        self.screen = setup.screen
        self.buttons = pg.sprite.Group()
        self.bg = utils.load_image("bg.jpg")
        self.bg = pg.transform.scale(self.bg, (constants.width, constants.height))
        rect = self.screen.get_rect()
        checkbox.CheckBox(self.buttons, "Show FPS", rect)

    def update(self, keys, clicks):
        self.screen.blit(self.bg, (0, 0))
        self.buttons.draw(self.screen)
        for i in self.buttons:
            state = i.update(clicks)
            if state:
                settings[self.states[state[0]]] = state[1]
        if keys[pg.K_ESCAPE]:
            return "back"


class Levels:
    def __init__(self):
        self.states = {"Level 1": "level1",
                       "Level 2": "level2"}
        self.screen = setup.screen
        self.buttons = pg.sprite.Group()
        self.bg = utils.load_image("bg.jpg")
        self.bg = pg.transform.scale(self.bg, (constants.width, constants.height))
        rect = self.screen.get_rect()
        rect.y -= 15
        button.Button(self.buttons, "Level 1", rect)
        rect.y += 60
        button.Button(self.buttons, "Level 2", rect)
        self.x = 0
        self.y = 0

    def update(self, keys, clicks):
        self.screen.blit(self.bg, (0, 0))
        self.buttons.draw(self.screen)
        if keys[pg.K_ESCAPE]:
            return "back"
        for i in self.buttons:
            state = i.update(clicks)
            if state:
                return self.states[state]
