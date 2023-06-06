import pygame as pg
from settings import *
from library import *
from menu import *

class Main:
    def __init__(self):
        self.running = True
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        self.body = Body(self)
        self.clock = pg.time.Clock()
        self.menu = Menu(self)

        self.score = 0
    

    def update(self):
        if not self.menu.running:
            self.delta_time = self.clock.tick(FPS)
            pg.display.set_caption(f'FPS: [{round(self.clock.get_fps(), 1)}],       SCORE: [{self.score}]')
            self.draw()
            pg.display.flip()

    def draw(self):
        self.window.fill('sky blue')
        #self.window.blit(sky_background, (0, 0))
        self.body.draw()


    def check_events(self):
        self.events = pg.event.get()
        for e in self.events:
            if e.type == pg.QUIT:
                self.running = False


    def run(self):
        while self.running:
            self.check_events()
            if not self.menu.running:
                self.update()
            else:
                self.menu.update()


if __name__ == '__main__':
    game = Main()
    game.run()
