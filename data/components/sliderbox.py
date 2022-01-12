import pygame as pg
from .. import setup
from .. import utils
from ..settings import settings


class SliderBox(pg.sprite.Sprite):
    def __init__(self, group, text, rect):
        super().__init__(group)
        self.screen = setup.screen
        self.font = pg.font.SysFont("Arial", 32)
        self.slider_box = pg.Rect(100, 100, 120, 20)
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color_hovered = pg.Color('dodgerblue3')
        self.color = self.color_active
        self.volume = settings["volume"]
        self.maxi = 100
        self.mini = 0
        self.rect = self.slider_box
        self.rect.center = rect.center
        self.center = self.rect.copy()
        self.rect.x += 150
        self.text = text
        self.old_time = 0.0
        self.time = pg.time.get_ticks()

    def update(self, clicks):
        utils.draw_text(f"{self.text}: {int(self.volume)}", 30, "white", self.screen, self.center)
        button_box = self.slider_box.copy()
        button_box.width = 20

        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.color = self.color_hovered
        else:
            self.color = self.color_active

        if clicks[0]:
            if self.rect.collidepoint(pg.mouse.get_pos()):
                self.volume = (pg.mouse.get_pos()[0] - button_box.x - 10) / 80 * (self.maxi - self.mini) + self.mini
                if self.volume < self.mini:
                    self.volume = self.mini
                if self.volume > self.maxi:
                    self.volume = self.maxi

        button_box.x += self.volume
        pg.draw.rect(self.screen, self.color_inactive, self.slider_box)
        pg.draw.rect(self.screen, self.color, button_box)
        return self.text, int(self.volume)
