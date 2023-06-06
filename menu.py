from settings import *

class Menu:
    def __init__(self, main):
        self.main = main
        self.window = main.window
        self.running = True

        self.font_my_game = 'fonts/Gameplay.ttf'

        # TEXTS
        self.text_title = Text(self, 'Koobie\'s Quest', self.font_my_game, 100, 'yellow', (WIDTH/2, HEIGHT*.15), False)
        

    def update(self):
        self.display()

    def display(self):
        self.window.fill((15, 15, 15))
        self.window.blit(sky_background, (WIDTH/2 - (sky_background.get_width() / 2), 0))

        self.text_title.update()

        pg.display.flip()

class Text:
    def __init__(self, menu, text, font, fontsize, color, pos, clickable):
        self.menu = menu
        self.window = menu.window
        self.text = text
        self.color = color
        self.pos = pos
        self.clickable = clickable

        self.font = pg.font.Font(font, fontsize)

    def update(self):
        self.display()

    def display(self):
        self.text_title = pg.font.Font.render(self.font, self.text, False, self.color)
        pos = (self.pos[0] - self.text_title.get_width()/2, self.pos[1] - self.text_title.get_height()/2)
        self.window.blit(self.text_title, pos)