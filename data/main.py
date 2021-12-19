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
        self.states = states
        self.state = self.states["menu"]

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        self.screen.fill((0, 0, 0))
        self.state.render()
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
