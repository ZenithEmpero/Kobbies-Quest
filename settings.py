import pygame as pg

FPS = 60

WIDTH = 1200
HEIGHT = 600

player_speed = 0.2
obstacle_speed = 0.25

#IMAGES
sky_background = pg.image.load('textures/bg2.png')
x = 4
sky_background = pg.transform.scale(sky_background, (sky_background.get_width()*x, sky_background.get_height()*x))

hitbox_color = 'green'