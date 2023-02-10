import pygame
from level import Level

map1 = open("maps/map1.txt").readlines()
size_x = 50
width = 1920
f = open("maps//map1.txt", mode="rt")
data = f.readlines()
map_w = len(data[17]) * size_x
height = len(data) * size_x
size = width, height
screen = pygame.display.set_mode(size)
level = Level(map1, screen, 'game')



