import pygame

from . import constants
from . import setup
from .states import menu
import pygame as pg


class Control:
    def __init__(self, states):
        self.screen = setup.screen
        self.running = True
        self.clock = pg.time.Clock()
        self.fps = constants.fps
        self.keys = pg.key.get_pressed()
        self.clicks = pg.mouse.get_pressed()
        self.states = states
        self.previous = None
        self.state = self.states["menu"]

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
            if event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.clicks = pg.mouse.get_pressed()
            if event.type == pg.MOUSEBUTTONUP:
                self.clicks = pg.mouse.get_pressed()

    def update(self):
        self.screen.fill((0, 0, 0))
        state = self.state.update(self.keys, self.clicks)
        if state == "exit":
            self.running = False
        elif state == "back":
            self.state = self.previous
            self.previous = None
        elif state:
            self.previous = self.state
            self.state = self.states[state]
        pg.display.update()

    def main(self):
        while self.running:
            self.event_loop()
            self.update()
            self.clock.tick(self.fps)


def main():
    states = {"menu": menu.Menu(),
              "options": menu.Options()}

    control = Control(states)
    control.main()
