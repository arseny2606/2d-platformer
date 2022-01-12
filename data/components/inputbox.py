import pygame as pg
from .. import setup
from .. import utils
from ..settings import settings


class InputBox(pg.sprite.Sprite):
    def __init__(self, group, text, rect):
        super().__init__(group)
        self.screen = setup.screen
        self.font = pg.font.SysFont("Arial", 32)
        self.input_box = pg.Rect(100, 100, 140, 32)
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.nick = settings['nickname']
        self.rect = self.input_box
        self.rect.center = rect.center
        self.center = self.rect.copy()
        self.rect.x += 150
        self.text = text
        self.old_time = 0.0
        self.time = pg.time.get_ticks()

    def update(self, clicks, keys, key_events):
        self.time = pg.time.get_ticks()
        utils.draw_text(self.text, 30, "white", self.screen, self.center)
        if self.old_time + 120 < self.time:
            if clicks[0]:
                if self.rect.collidepoint(pg.mouse.get_pos()):
                    self.old_time = self.time
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.color_active if self.active else self.color_inactive
        for event in key_events:
            if self.active:
                if event.key == pg.K_RETURN:
                    return self.text, self.nick
                elif event.key == pg.K_BACKSPACE:
                    self.nick = self.nick[:-1]
                else:
                    self.nick += event.unicode
        txt_surface = self.font.render(self.nick, True, self.color)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y))
        pg.draw.rect(self.screen, self.color, self.input_box, 2)
        return self.text, self.nick
