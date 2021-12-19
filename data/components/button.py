import pygame as pg
from .. import setup
from .. import utils


class Button(pg.sprite.Sprite):
    def __init__(self, group, text, rect):
        super().__init__(group)
        self.screen = setup.screen
        self.image = utils.load_image("button.png")
        self.rect = self.image.get_rect()
        self.rect.center = rect.center
        self.text = text

    def update(self):
        utils.draw_text(self.text, 30, "white", self.screen, self.rect)
