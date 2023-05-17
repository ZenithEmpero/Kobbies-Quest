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


    def draw(self):
        self.obstacle1.draw()
        self.obstacle2.draw()
        self.water.draw()
        self.player.draw()



class Pillar:
    def __init__(self, body, pos):
        self.main = body.main
        self.window = self.main.window
        self.body = body
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
        self.speed = self.body.speed
        self.coordinate = (self.coordinate[0] - self.speed * self.main.delta_time, self.coordinate[1])

        if self.coordinate[0] < -200:
            self.coordinate = (1300, r.randint(200, 500))

    def speed_increase(self):
            while self.main.running:
                pg.time.wait(5000)
                self.body.speed += 0.01

class Player:
    def __init__(self, body):
        self.player_pos = (200, 300)
        self.body = body
        self.main = body.main
        

    def draw(self):
        pg.draw.circle(self.main.window, 'red', self.player_pos, 25)

    def controls(self):
        pass

class Water:
    def __init__(self, body):
        self.body = body
        self.main = body.main
        self.water_pos = (0, 400)

        self.x = 0
        self.y = 500

    def draw(self):
        self.draw_water_rect()

    def draw_water_rect(self):
        self.sin_wave()
        self.water_rect = pg.Rect(self.water_pos[0], self.water_pos[1], 1200, self.y)
        pg.draw.rect(self.main.window, 'blue', self.water_rect)


    def sin_wave(self):
        self.y = self.body.player.player_pos[1]
        self.x += 1 * self.main.delta_time
        self.y += m.sin(self.x) * self.main.delta_time
