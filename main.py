import pygame as pg
from settings import *
from menu import *
from library import *

class Main:
    def __init__(self):
        pg.font.init()
        pg.init()
        pg.mixer.init()
        self.running = True
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        self.body = Body(self)
        self.clock = pg.time.Clock()
        self.menu = Menu(self)

        self.score = 0
        self.start = False

        # SPRITE
        sprite = MySprite(WIDTH/2, HEIGHT/2, .33)  # Specify the initial width and height of the sprite

        # Create a sprite group
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(sprite)

        # AUDIO
        self.forg_audio = pg.mixer.Sound('audio/oof.mp3')
        self.bgm = pg.mixer.Sound('audio/bgm.mp3')
        self.bgm.play(loops=-1)

    def update(self):
        if not self.menu.running:
            self.delta_time = self.clock.tick(FPS)
            pg.display.set_caption(f'FPS: [{round(self.clock.get_fps(), 1)}],       SCORE: [{self.score}]')
            self.draw()
            pg.display.flip()

    def draw(self):
        self.window.fill('sky blue')
        #self.window.blit(sky_background, (0, 0))

        if not self.menu.running:
            self.all_sprites.draw(self.window)
            self.body.obstacle1.update()
            self.body.obstacle2.update()
            if not self.start:
                self.body.obstacle1.start_again()
                self.body.obstacle2.start_again()
                self.start = True
            self.body.player.draw()
            self.body.water.draw()
            self.body.ui.update()
            self.body.collision.update()
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


class MySprite(pg.sprite.Sprite):
    def __init__(self, x, y, scale):
        pg.sprite.Sprite.__init__(self)
        self.original_image = pg.image.load('textures/bg4.jpg').convert_alpha()  # Load the sprite image
        self.image = pg.transform.scale(self.original_image, (self.original_image.get_width()*scale, self.original_image.get_height()*scale))  # Resize the image
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.center = (x, y)  # Set the initial position of the sprite

    def update(self):
        self.rect.x += 1  # Move the sprite horizontally


if __name__ == '__main__':
    game = Main()
    game.run()
    pg.quit()