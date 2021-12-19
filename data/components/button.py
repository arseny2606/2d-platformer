import pygame as pg
from .. import setup
from .. import utils


class Button(pg.sprite.Sprite):
    def __init__(self, group, text, rect):
        super().__init__(group)
        self.screen = setup.screen
        self.btn_image = utils.load_image("button.png")
        self.btn_hover_image = utils.load_image("button_hover.png")
        self.image = self.btn_image
        self.rect = self.image.get_rect()
        self.rect.center = rect.center
        self.text = text

    def update(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.image = self.btn_hover_image
        else:
            self.image = self.btn_image
        utils.draw_text(self.text, 30, "white", self.screen, self.rect)
