import pygame
from level import Level
import sys

# карта для уровня
map1 = open("graphics/map1.txt").readlines()
active_map = map1
pygame.init()

size_x = 50
width = 800
height = len(map1) * size_x

size = width, height
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

level = Level(map1, screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")
    level.run()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
