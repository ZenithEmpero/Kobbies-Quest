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
        self.player = body.player
        self.window = self.main.window
        
        self.health_pos_cons = (900, 20)

        self.health_duck = pg.image.load('textures/health_duck.png')
        self.health_skull = pg.image.load('textures/health_skull.png')
        self.health_duck = pg.transform.scale(self.health_duck, (40, 40))
        self.health_skull = pg.transform.scale(self.health_skull, (40, 40))

        self.game_over_img = pg.image.load('textures/game_over.png')
        self.game_over_img = pg.transform.scale(self.game_over_img, (200, 100))
        self.go_img_dim = self.game_over_img.get_width(), self.game_over_img.get_height()

        self.hd_dim = self.health_duck.get_width(), self.health_duck.get_height()
        self.hs_dim = self.health_skull.get_width(), self.health_skull.get_height()

    def update(self):
        self.draw()
        self.health()

    def draw(self):
        pass

    def health(self):
        pos_x = self.health_pos_cons[0]

        self.player_health = self.player.health
        j = self.player_health
        for i in range(0, 3):
            if j > 0:
                self.health_draw(self.health_duck, pos_x)
            else:
                self.health_draw(self.health_skull, pos_x)

            pos_x += 60
            j -= 1

        if self.player_health <= 0:
            self.window.blit(self.game_over_img, (600 - self.go_img_dim[0] / 2, 300 - self.go_img_dim[1] / 2))



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
        self.pillar_img_dim = self.pillar_img.get_width(), self.pillar_img.get_height()

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

        self.damage_animation = False
        self.show_image = True
        self.da = 0

        self.go_sec = -200

    def draw(self):
        #pg.draw.circle(self.main.window, 'red', self.player_pos, 25)
        self.rotate_image()

        if self.show_image:
            self.main.window.blit(self.duck_image, (self.player_pos[0] - self.rotated_duck_rect.width / 2, self.player_pos[1] - self.rotated_duck_rect.height / 2))
        #pg.draw.circle(self.main.window, 'red', self.player_pos, 2)
        self.controls()

        self.check_if_alive()
        self.play_damage_animation(0.25)

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

        if self.health >= 1:
            self.rot = m.sin(self.rot_x) * 14
            self.rot_x += 0.005 * self.main.delta_time

    def check_if_alive(self):
        if self.health <= 0:
            self.alive = False

    def play_damage_animation(self, x):
        if self.damage_animation:
            self.da += 0.05 * self.main.delta_time
            self.da_sin = m.sin(self.da)
            if self.da_sin > 0:
                self.show_image = False
            else:
                self.show_image = True
        else:
            self.show_image = True


    def game_over(self):
        original_y = self.player_pos[1]
        y = original_y
        pg.time.wait(2000)
        for i in range(0, 1000):
            self.go_sec += .1 * self.main.delta_time




class Water:
    def __init__(self, body):
        self.body = body
        self.main = body.main
        self.window = self.main.window
        self.player = body.player
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
        if self.player.health >= 1:
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


        self.recent_player_collision = None


    def update(self):
        self.position_collision_rect()
        #self.draw()
        self.detect_collision()

    def draw(self):
        pg.draw.rect(self.window, hitbox_color, self.player_rect, width=4)
        pg.draw.rect(self.window, hitbox_color, self.ob1_rect, width=4)
        pg.draw.rect(self.window, hitbox_color, self.ob1_rect_top, width=4)
        pg.draw.rect(self.window, hitbox_color, self.ob2_rect, width=4)
        pg.draw.rect(self.window, hitbox_color, self.ob2_rect_top, width=4)

    def position_collision_rect(self):
        # PLAYER COLLISION
        size_reduction_rate = .4
        reduced_size = self.player.duck_dim[0] - (self.player.duck_dim[0] * size_reduction_rate), self.player.duck_dim[1] - (self.player.duck_dim[1] * size_reduction_rate)
        adjust_pos = self.player.player_pos[0] - (reduced_size[0] // 2), self.player.player_pos[1] - (reduced_size[1] // 2)
        self.player_rect = pg.Rect(adjust_pos[0], adjust_pos[1], reduced_size[0], reduced_size[1])

        # OBSTACLE 1 COLLISION
        size = self.ob1.pillar_img_dim[0], self.ob1.pillar_img_dim[1]
        ob1_pos = self.ob1.coordinate[0], self.ob1.coordinate[1]
        self.ob1_rect = pg.Rect(ob1_pos[0], ob1_pos[1], size[0], size[1])
        self.ob1_rect_top = pg.Rect(ob1_pos[0], ob1_pos[1] - (self.ob1.gap), size[0], size[1])

        # OBSTACLE 2 COLLISION
        size = self.ob2.pillar_img_dim[0], self.ob2.pillar_img_dim[1]
        ob2_pos = self.ob2.coordinate[0], self.ob2.coordinate[1]
        self.ob2_rect = pg.Rect(ob2_pos[0], ob2_pos[1], size[0], size[1])
        self.ob2_rect_top = pg.Rect(ob2_pos[0], ob2_pos[1] - (self.ob2.gap), size[0], size[1])

        self.ob1_rects = [self.ob1_rect, self.ob1_rect_top]
        self.ob2_rects = [self.ob2_rect, self.ob2_rect_top]

    def detect_collision(self):
        for i in self.ob1_rects:
            if self.recent_player_collision != 1:
                if self.player_rect.colliderect(i):
                    self.player.health -= 1
                    if self.player.health >= 1:
                        Thread(target= self.reverse_damage_animation).start()
                    self.recent_player_collision = 1

        for i in self.ob2_rects:
            if self.recent_player_collision != 2:
                if self.player_rect.colliderect(i):
                    self.player.health -= 1
                    if self.player.health >= 1:
                        Thread(target= self.reverse_damage_animation).start()
                    self.recent_player_collision = 2

    def reverse_damage_animation(self):
        self.player.damage_animation = True
        pg.time.wait(1000)
        self.player.damage_animation = False