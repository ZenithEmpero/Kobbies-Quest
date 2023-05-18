import pygame as pg
import time as t
import random as r
import math as m
import sys
from settings import *
from threading import Thread

class Body:
    def __init__(self, main):
        self.window = main.window
        self.speed = obstacle_speed
        self.main = main
        self.player = Player(self)
        self.water = Water(self)

        y1 = r.randint(200, 500)
        y2 = r.randint(200, 500)


        self.obstacle1 = Pillar(self, (1300, y1))
        self.obstacle2 = Pillar(self, (2050, y2))


        self.ui = UI(self)
        self.collision = Collision(self)

    def draw(self):
        self.obstacle1.draw()
        self.obstacle2.draw()
        self.player.draw()
        self.water.draw()
        self.ui.update()
        self.collision.update()


class UI:
    def __init__(self, body):
        self.body = body
        self.main = body.main
        self.window = self.main.window
        
        self.health_pos_cons = (900, 20)

        self.health_duck = pg.image.load('textures/health_duck.png')
        self.health_skull = pg.image.load('textures/health_skull.png')
        self.health_duck = pg.transform.scale(self.health_duck, (40, 40))
        self.health_skull = pg.transform.scale(self.health_skull, (150, 150))

        self.hd_dim = self.health_duck.get_width(), self.health_duck.get_height()
        self.hs_dim = self.health_skull.get_width(), self.health_skull.get_height()

    def update(self):
        self.draw()
        self.health()

    def draw(self):
        pass

    def health(self):
        self.healths = {1 : True, 2 : True, 3 : True}
        x = self.health_pos_cons[0]
        for i in self.healths:
            if self.healths[1]:
                self.health_draw(self.health_duck, x)
            elif self.healths[1] == False:
                self.health_draw(self.health_skull, x)
            x += self.hd_dim[0] + (self.hd_dim[0] / 2)


    def health_draw(self, image, x):
        self.window.blit(image, (x, self.health_pos_cons[1]))



class Pillar:
    def __init__(self, body, pos):
        self.main = body.main
        self.window = self.main.window
        self.body = body
        self.player = body.player
        self.coordinate = pos
        self.gap = 600

        self.pillar_img = pg.image.load('textures/pillar.png')
        self.top_pillar_img = pg.transform.rotate(self.pillar_img, 180)

        Thread(target= self.speed_increase).start()
       

    def draw(self):
        self.movement()
        self.window.blit(self.pillar_img, (self.coordinate[0], self.coordinate[1]))
        self.window.blit(self.top_pillar_img, (self.coordinate[0], self.coordinate[1] - self.gap))

    def movement(self):
        if self.player.alive:
            self.speed = self.body.speed
            self.coordinate = (self.coordinate[0] - self.speed * self.main.delta_time, self.coordinate[1])

            if self.coordinate[0] < -200:
                self.coordinate = (1300, r.randint(200, 500))

    def speed_increase(self):
            while self.main.running:
                pg.time.wait(10000)
                self.body.speed += 0.01

class Player:
    def __init__(self, body):
        self.player_pos = (200, 100)
        self.body = body
        self.main = body.main
        self.health = 3
        self.alive = True
        self.duck_image = pg.image.load('textures/duck.png')
        self.duck_image = pg.transform.scale(self.duck_image, (60, 60))
        self.or_duck_image = self.duck_image
        self.duck_rect = self.or_duck_image.get_rect()


        self.duck_dim = self.duck_image.get_width(), self.duck_image.get_height()

        self.x = self.player_pos[0]
        self.y = self.player_pos[1]

        self.drag = 0

        self.rise = False
        self.rot = 0
        self.rot_x = 0

    def draw(self):
        #pg.draw.circle(self.main.window, 'red', self.player_pos, 25)
        self.rotate_image()
        self.main.window.blit(self.duck_image, (self.player_pos[0] - self.rotated_duck_rect.width / 2, self.player_pos[1] - self.rotated_duck_rect.height / 2))
        pg.draw.circle(self.main.window, 'red', self.player_pos, 2)
        self.controls()

    def controls(self):
        if self.alive:
            keys = pg.key.get_pressed()
            speed = self.drag * player_speed
            if keys[pg.K_SPACE]:
                self.drag -= 0.1
                if self.drag < -1:
                    self.drag = -1
            else:
                self.drag += 0.1
                if self.drag > 1:
                    self.drag = 1

            self.y += speed * self.main.delta_time
            if self.y > 565:
                self.y = 565
            if self.y < 35:
                self.y = 35
            self.player_pos = (self.x, self.y)

    def rotate_image(self):
        self.duck_image = pg.transform.rotate(self.or_duck_image, self.rot)
        self.rotated_duck_rect = self.duck_image.get_rect()
        self.rotated_pos = self.rotated_duck_rect.center

        self.rot = m.sin(self.rot_x) * 14
        self.rot_x += 0.005 * self.main.delta_time


class Water:
    def __init__(self, body):
        self.body = body
        self.main = body.main
        self.window = self.main.window
        self.water_pos = (0, 400)

        self.x = 0
        self.y = self.water_pos[1]

    def draw(self):
        self.draw_water_rect()

    def draw_water_rect(self):
        self.sin_wave()
        self.water_rect = pg.Surface((1200, 1000), pg.SRCALPHA)
        self.water_rect.fill((0, 0, 255, 128))
        self.window.blit(self.water_rect, self.water_pos)


    def sin_wave(self):
        self.y = self.body.player.player_pos[1] + 14
        self.x += .004 * self.main.delta_time
        self.y += m.sin(self.x) * 6 #* self.main.delta_time
        self.water_pos = (0, self.y)
    
class Collision:
    def __init__(self, body):
        self.body = body
        self.main = body.main
        self.player = body.player
        self.ob1 = body.obstacle1
        self.ob2 = body.obstacle2
        self.window = self.main.window



    def update(self):
        self.position_collision_rect()
        #self.draw()

    def draw(self):
        pg.draw.rect(self.window, hitbox_color, self.player_rect, width=4)

    def position_collision_rect(self):
        # PLAYER COLLISION
        size_reduction_rate = .4
        reduced_size = self.player.duck_dim[0] - (self.player.duck_dim[0] * size_reduction_rate), self.player.duck_dim[1] - (self.player.duck_dim[1] * size_reduction_rate)
        adjust_pos = self.player.player_pos[0] - (reduced_size[0] // 2), self.player.player_pos[1] - (reduced_size[1] // 2)
        self.player_rect = pg.Rect(adjust_pos[0], adjust_pos[1], reduced_size[0], reduced_size[1])

        # OBSTACLE 1 COLLISION
        #self.ob1_rect = pg.Rect()