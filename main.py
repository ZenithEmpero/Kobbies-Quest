import pygame as pg
import sys
from settings import *
from library import *


class Main:
    def __init__(self):
        self.running = True
        self.window = pg.display.set_mode((WIDTH, HEIGHT), flags=pg.RESIZABLE)
        self.body = Body(self)
        self.clock = pg.time.Clock()
        


    def update(self):
        self.delta_time = self.clock.tick(FPS)
        self.draw()

        pg.display.flip()

    def draw(self):
        self.window.fill('black')
        self.window.blit(sky_background, (0, 0))
        self.body.draw()


    def check_events(self):
        for events in pg.event.get():
            if events.type == pg.QUIT:
                self.running = False


    def run(self):
        while self.running:
            self.check_events()
            self.update()


if __name__ == '__main__':
    game = Main()
    game.run()
