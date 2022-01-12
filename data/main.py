import pygame as pg
import json

from . import constants
from . import setup
from .settings import settings
from .states import menu
from .states.levels import level1
from .states.levels import level2
from .states.levels import infinite


def load_settings():
    with open("resources/data/settings.json") as f:
        new_settings = json.load(f)
        for i in new_settings.items():
            settings[i[0]] = i[1]


def save_settings():
    with open("resources/data/settings.json", "w") as f:
        json.dump(settings, f, indent=4)


class Control:
    def __init__(self, states):
        self.screen = setup.screen
        self.running = True
        self.clock = pg.time.Clock()
        self.fps = constants.fps
        self.keys = pg.key.get_pressed()
        self.clicks = pg.mouse.get_pressed()
        self.states = states
        self.previous = []
        self.state = self.states["menu"]
        if callable(self.state):
            self.state = self.state()
        self.font = pg.font.SysFont("Arial", 25)
        self.fps_text = None

    def event_loop(self):
        key_events = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                save_settings()
            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                key_events.append(event)
            if event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.clicks = pg.mouse.get_pressed()
            if event.type == pg.MOUSEBUTTONUP:
                self.clicks = pg.mouse.get_pressed()
        return key_events

    def update(self, key_events):
        self.screen.fill((0, 0, 0))
        if self.state == self.states["options"]:
            state = self.state.update(self.keys, self.clicks, key_events)
        else:
            state = self.state.update(self.keys, self.clicks)
        if state == "exit":
            self.running = False
            save_settings()
        elif state == "back":
            self.state = self.previous[-1]
            if callable(self.state):
                self.state = self.state()
            del self.previous[-1]
        elif state:
            self.previous.append(self.state)
            self.state = self.states[state]
            if callable(self.state):
                self.state = self.state()
        if self.fps_text is not None:
            self.screen.blit(self.fps_text, (10, 0))
        pg.display.update()

    def main(self):
        while self.running:
            key_events = self.event_loop()
            self.update(key_events)
            self.clock.tick(self.fps)
            if settings["show_fps"]:
                fps = self.clock.get_fps()
                self.fps_text = self.font.render(str(int(fps)), True, pg.Color("coral"))
            else:
                pg.display.set_caption(constants.name)
                self.fps_text = None


def main():
    load_settings()
    states = {"menu": menu.Menu(),
              "options": menu.Options(),
              "leaderboard": menu.Leaderboard(),
              "story": menu.Levels(),
              "level1": level1.Level1,
              "level2": level2.Level2,
              "infinite": infinite.InfiniteLevel}
    control = Control(states)
    control.main()
