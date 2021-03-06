import json

import pygame as pg
from .. import setup
from ..components import button, checkbox, inputbox, sliderbox
from .. import utils
from .. import constants
from ..settings import settings


class Menu:
    def __init__(self):
        self.states = {"Story mode": "story",
                       "Infinite mode": "infinite",
                       "Leaderboard": "leaderboard",
                       "Infinite leaderboard": "infinite_leaderboard",
                       "Options": "options",
                       "Exit": "exit"}
        self.screen = setup.screen
        self.buttons = pg.sprite.Group()
        self.bg = utils.load_image("bg.jpg")
        self.bg = pg.transform.scale(self.bg, (constants.width, constants.height))
        pg.mixer.music.load("resources/sounds/menu.mp3")
        pg.mixer.music.play(-1)
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
            if self.loader >= constants.width - 100:
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
                       "Save": "save",
                       "Volume": "volume"}
        self.screen = setup.screen
        self.buttons = pg.sprite.Group()
        self.checkboxes = pg.sprite.Group()
        self.inputboxes = pg.sprite.Group()
        self.sliderboxes = pg.sprite.Group()
        self.bg = utils.load_image("bg.jpg")
        self.bg = pg.transform.scale(self.bg, (constants.width, constants.height))
        rect = self.screen.get_rect()
        rect.y -= 60
        checkbox.CheckBox(self.checkboxes, "Show FPS", rect, settings["show_fps"])
        rect.y += 60
        inputbox.InputBox(self.inputboxes, "NickName", rect)
        rect.y += 60
        sliderbox.SliderBox(self.sliderboxes, "Volume", rect)
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
        for i in self.sliderboxes:
            volume = i.update(clicks)
            if volume:
                settings[self.states[volume[0]]] = volume[1]
                pg.mixer.music.set_volume(settings["volume"] / 100)
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
        self.font = pg.font.SysFont("Arial", 30)
        self.buttons = pg.sprite.Group()
        rect = self.screen.get_rect()
        rect.y += constants.height // 3
        button.Button(self.buttons, "Infinite game", rect)

    def update(self, keys, clicks):
        self.screen.blit(self.bg, (0, 0))
        self.buttons.draw(self.screen)
        with open("resources/data/leaderboard.json") as f:
            data = json.load(f)
            leaderboard = data["users"]
            leaderboard_1 = list(filter(lambda x: x["level"] == 1, leaderboard))
            leaderboard_1.sort(key=lambda x: x["score"], reverse=True)
            leaderboard_1 = leaderboard_1[:10]
            y = constants.height // 4
            text = self.font.render("Level 1:", True,
                                    pg.Color("red"))
            self.screen.blit(text, (text.get_rect(center=(constants.width // 4, y))))
            y += constants.height // 20
            if len(leaderboard_1) == 0:
                text = self.font.render("There is no results", True,
                                        pg.Color("red"))
                self.screen.blit(text, (text.get_rect(center=(constants.width // 4, y))))
                y += constants.height // 20
                text = self.font.render("Be the first to set a record!", True,
                                        pg.Color("red"))
                self.screen.blit(text, (text.get_rect(center=(constants.width // 4, y))))
            for i in leaderboard_1:
                if len(i['name']) > 30:
                    i['name'] = i['name'][:30] + '...'
                text = self.font.render(f"{i['name']} {i['time']} - {i['score']}", True,
                                        pg.Color("red"))
                self.screen.blit(text, (text.get_rect(center=(constants.width // 4, y))))
                y += constants.height // 20
            leaderboard_2 = list(filter(lambda x: x["level"] == 2, leaderboard))
            leaderboard_2.sort(key=lambda x: x["score"], reverse=True)
            leaderboard_2 = leaderboard_2[:10]
            y = constants.height // 4
            text = self.font.render("Level 2:", True,
                                    pg.Color("red"))
            self.screen.blit(text, (text.get_rect(center=(constants.width // 4 * 3, y))))
            y += constants.height // 20
            if len(leaderboard_2) == 0:
                text = self.font.render("There is no results", True,
                                        pg.Color("red"))
                self.screen.blit(text, (text.get_rect(center=(constants.width // 4 * 3, y))))
                y += constants.height // 20
                text = self.font.render("Be the first to set a record!", True,
                                        pg.Color("red"))
                self.screen.blit(text, (text.get_rect(center=(constants.width // 4 * 3, y))))
            for i in leaderboard_2:
                if len(i['name']) > 30:
                    i['name'] = i['name'][:30] + '...'
                text = self.font.render(f"{i['name']} {i['time']} - {i['score']}", True,
                                        pg.Color("red"))
                self.screen.blit(text, (text.get_rect(center=(constants.width // 4 * 3, y))))
                y += constants.height // 20
        for i in self.buttons:
            state = i.update(clicks)
            if state:
                return "infinite_leaderboard"
        if keys[pg.K_ESCAPE]:
            return "back"


class InfiniteLeaderboard:
    def __init__(self):
        self.screen = setup.screen
        self.bg = utils.load_image("bg.jpg")
        self.bg = pg.transform.scale(self.bg, (constants.width, constants.height))
        self.font = pg.font.SysFont("Arial", 30)
        self.buttons = pg.sprite.Group()
        rect = self.screen.get_rect()
        rect.y += constants.height // 3
        b1 = button.Button(self.buttons, "Back", rect)
        b1.rect.y += b1.rect.height

    def update(self, keys, clicks):
        self.screen.blit(self.bg, (0, 0))
        self.buttons.draw(self.screen)
        with open("resources/data/leaderboard.json") as f:
            data = json.load(f)
            leaderboard = data["users"]
            leaderboard = list(filter(lambda x: x["level"] == -1, leaderboard))
            leaderboard.sort(key=lambda x: x["score"], reverse=True)
            leaderboard = leaderboard[:10]
            y = constants.height // 4
            text = self.font.render("Infinite game:", True,
                                    pg.Color("red"))
            self.screen.blit(text, (text.get_rect(center=(constants.width // 2, y))))
            y += constants.height // 20
            if len(leaderboard) == 0:
                text = self.font.render("There is no results", True,
                                        pg.Color("red"))
                self.screen.blit(text, (text.get_rect(center=(constants.width // 2, y))))
                y += constants.height // 20
                text = self.font.render("Be the first to set a record!", True,
                                        pg.Color("red"))
                self.screen.blit(text, (text.get_rect(center=(constants.width // 2, y))))
            for i in leaderboard:
                if len(i['name']) > 30:
                    i['name'] = i['name'][:30] + '...'
                text = self.font.render(f"{i['name']} {i['time']} - {i['score']}", True,
                                        pg.Color("red"))
                self.screen.blit(text, (text.get_rect(center=(constants.width // 2, y))))
                y += constants.height // 20
        for i in self.buttons:
            state = i.update(clicks)
            if state:
                return "back"
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
