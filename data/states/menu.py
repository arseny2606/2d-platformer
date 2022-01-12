import json

import pygame as pg
from .. import setup
from ..components import button, checkbox, inputbox
from .. import utils
from .. import constants
from ..settings import settings


class Menu:
    def __init__(self):
        self.states = {"Story mode": "story",
                       "Infinite mode": "infinite",
                       "Leaderboard": "leaderboard",
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
        button.Button(self.buttons, "Leaderboard", rect)
        rect.y += 60
        button.Button(self.buttons, "Options", rect)
        rect.y += 60
        button.Button(self.buttons, "Exit", rect)
        self.x = 0
        self.y = 0
        self.loading = True
        self.loader = 10

    def update(self, keys, clicks):
        self.screen.blit(self.bg, (0, 0))
        if self.loading:
            pg.draw.rect(self.screen, "red", [100, constants.height // 2 - 5, self.loader, 10])
            self.loader += 10
            if self.loader >= 1080:
                self.loading = False
            return
        self.buttons.draw(self.screen)
        for i in self.buttons:
            state = i.update(clicks)
            if state:
                return self.states[state]
        return False


class Options:
    def __init__(self):
        self.states = {"Show FPS": "show_fps",
                       "NickName": "nickname",
                       "Save": "save"}
        self.screen = setup.screen
        self.buttons = pg.sprite.Group()
        self.checkboxes = pg.sprite.Group()
        self.inputboxes = pg.sprite.Group()
        self.bg = utils.load_image("bg.jpg")
        self.bg = pg.transform.scale(self.bg, (constants.width, constants.height))
        rect = self.screen.get_rect()
        rect.y -= 30
        checkbox.CheckBox(self.checkboxes, "Show FPS", rect, settings["show_fps"])
        rect.y += 60
        inputbox.InputBox(self.inputboxes, "NickName", rect)
        rect.y += 180
        button.Button(self.buttons, "Save", rect)

    def update(self, keys, clicks, key_events):
        self.screen.blit(self.bg, (0, 0))
        self.buttons.draw(self.screen)
        self.checkboxes.draw(self.screen)
        for i in self.checkboxes:
            state = i.update(clicks)
            if state:
                settings[self.states[state[0]]] = state[1]
        for i in self.inputboxes:
            nickname = i.update(clicks, keys, key_events)
            if nickname:
                settings[self.states[nickname[0]]] = nickname[1]
        self.buttons.draw(self.screen)
        for i in self.buttons:
            state = i.update(clicks)
            if state:
                for j in self.inputboxes:
                    settings["nickname"] = j.update(clicks, keys, key_events)[1]
                return "back"
        if keys[pg.K_ESCAPE]:
            return "back"


class Leaderboard:
    def __init__(self):
        self.screen = setup.screen
        self.bg = utils.load_image("bg.jpg")
        self.bg = pg.transform.scale(self.bg, (constants.width, constants.height))
        self.font = pg.font.SysFont("Arial", 60)

    def update(self, keys, clicks):
        self.screen.blit(self.bg, (0, 0))
        with open("resources/data/leaderboard.json") as f:
            data = json.load(f)
            leaderboard = data["users"]
            leaderboard.sort(key=lambda x: x["score"], reverse=True)
            leaderboard = leaderboard[:10]
            y = constants.height // 3
            for i in leaderboard:
                text = self.font.render(f"{i['name']} - {i['score']}", True, pg.Color("red"))
                self.screen.blit(text, (text.get_rect(center=(constants.width // 2, y))))
                y += constants.height // 15
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
