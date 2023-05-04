import pygame as pg
import time as t
import random as r
import sys
from settings import *
from threading import Thread

class Body:
    def __init__(self, main):
        self.window = main.window
        self.speed = obstacle_speed

        y1 = r.randint(200, 500)
        y2 = r.randint(200, 500)


        self.obstacle1 = Pillar(main, self, (1300, y1))
        self.obstacle2 = Pillar(main, self, (2050, y2))


    def draw(self):
        self.obstacle1.draw()
        self.obstacle2.draw()



class Pillar:
    def __init__(self, main, body, pos):
        self.window = main.window
        self.main = main
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

