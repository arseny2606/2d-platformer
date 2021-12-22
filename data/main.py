import pygame as pg

from . import constants
from . import setup
from .settings import settings
from .states import menu


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
        self.font = pg.font.SysFont("Arial", 25)
        self.fps_text = None

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
        if self.fps_text is not None:
            self.screen.blit(self.fps_text, (10, 0))
        pg.display.update()

    def main(self):
        while self.running:
            self.event_loop()
            self.update()
            self.clock.tick(self.fps)
            if settings["show_fps"]:
                fps = self.clock.get_fps()
                self.fps_text = self.font.render(str(int(fps)), True, pg.Color("coral"))
            else:
                pg.display.set_caption(constants.name)
                self.fps_text = None


def main():
    states = {"menu": menu.Menu(),
              "options": menu.Options()}

    control = Control(states)
    control.main()
