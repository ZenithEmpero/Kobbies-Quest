from settings import *



class Menu:
    def __init__(self, main):
        self.main = main
        self.window = main.window
        self.running = True

        self.font_gameplay = 'fonts/Gameplay.ttf'
        self.font_my_game = 'fonts/my game.ttf'
        self.font_8bi = 'fonts/8bi.ttf'
        self.font_ka1 = 'fonts/ka1.ttf'

        # TEXTS
        self.text_title2 = self.text_title = Text(self, 'Koobie\'s Quest', self.font_ka1, 100, 'yellow', (WIDTH/2 - 10, HEIGHT*.15 - 10), False, False)
        self.text_title = Text(self, 'Koobie\'s Quest', self.font_ka1, 100, 'black', (WIDTH/2, HEIGHT*.15), False, True)
        self.text_start2 = Text(self, 'Start', self.font_my_game, 70, 'black', (WIDTH/2 + 5, HEIGHT*.5 + 5), False, False)
        self.text_start = Text(self, 'Start', self.font_my_game, 70, 'white', (WIDTH/2, HEIGHT*.5), True, True)
        self.text_exit2 = Text(self, 'Exit', self.font_my_game, 70, 'black', (WIDTH/2 + 5, HEIGHT*.7 + 5), False, False)
        self.text_exit = Text(self, 'Exit', self.font_my_game, 70, 'white', (WIDTH/2, HEIGHT*.7), True, True)

    def update(self):
        self.display()
        self.check_click_event()
        self.mouse_state()

    def display(self):
        self.window.fill((15, 15, 15))
        self.window.blit(sky_background, (WIDTH/2 - (sky_background.get_width() / 2), 0))

        
        self.text_title.update()
        self.text_title2.update()
        self.text_start2.update()
        self.text_start.update()
        self.text_exit2.update()
        self.text_exit.update()

        pg.display.flip()

    def check_click_event(self):
        if self.text_start.clicked:
            self.running = False
            self.text_start.clicked = False
            self.main.body.ui.start_again()

        if self.text_exit.clicked:
            self.main.running = False

    def mouse_state(self):
        x = 0
        for i in [self.text_start.rect, self.text_exit.rect]:
            if i.collidepoint(self.text_exit.mouse_pos):
                x += 1
        if x > 0:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        else:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

class Text:
    def __init__(self, menu, text, font, fontsize, color, pos, clickable, setcursor):
        self.menu = menu
        self.window = menu.window
        self.text = text
        self.color = color
        self.pos = pos
        self.clickable = clickable
        self.clicked = False
        self.setcursor = setcursor

        self.font = pg.font.Font(font, fontsize)
        self.text_title = pg.font.Font.render(self.font, self.text, False, self.color)
        self.rect = self.text_title.get_rect()
        self.pos = (self.pos[0] - self.text_title.get_width()/2, self.pos[1] - self.text_title.get_height()/2)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        self.mouse_in_rect = False

    def update(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.display()
        self.click_event()

    def display(self):
        self.window.blit(self.text_title, self.pos)

    def click_event(self):
        if self.clickable:
            if self.rect.collidepoint(self.mouse_pos):
                for events in pg.event.get():
                    if events.type == pg.MOUSEBUTTONUP:
                        print(f'{self.text} clicked')
                        self.clicked = True
                