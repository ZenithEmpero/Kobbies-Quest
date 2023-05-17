import pygame as pg

FPS = 60

WIDTH = 1200
HEIGHT = 600

player_speed = 0.2
obstacle_speed = 0.25

#IMAGES
sky_background = pg.image.load('textures/sky.png')
sky_background = pg.transform.scale(sky_background, (1200, 800))