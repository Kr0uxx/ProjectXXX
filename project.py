import pygame
import sys
from level import Level
from display import Display
from menu import Menu

pygame.init()
running = True

# 4 состояния: game - в игре, start - на начальном экране, menu - в меню и dead - на экране смерти
status = 'game'

# карта для уровня
map1 = open("maps/map1.txt").readlines()
active_map = map1

size_x = 50
width = 1000
height = len(map1) * size_x

size = width, height
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

level = Level(map1, screen)
display = Display(screen, width, height, 100, 100)


# меню:

def quit_game():
    global running
    running = False


def resume_game():
    global status
    status = 'game'


def go_start_screen():
    pass


def open_settings():
    pass


menu = Menu(screen)
menu.append_option('Resume', resume_game)
menu.append_option('Settings', open_settings)
menu.append_option('Start Screen', go_start_screen)
menu.append_option('Quit', quit_game)

# графика
bg1 = pygame.image.load("graphics\\background_layer_1.png")
bg1 = pygame.transform.scale(bg1, (1280, 1080))
bg2 = pygame.image.load("graphics\\background_layer_2.png")
bg2 = pygame.transform.scale(bg2, (1280, 1080))
bg3 = pygame.image.load("graphics\\background_layer_3.png")
bg3 = pygame.transform.scale(bg3, (1280, 1080))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if status == 'game':
                if event.key == pygame.K_ESCAPE:
                    status = 'menu'
            elif status == 'menu':
                if event.key == pygame.K_w:
                    menu.switch(-1)
                elif event.key == pygame.K_s:
                    menu.switch(1)
                elif event.key == pygame.K_SPACE:
                    menu.select()
    if status == 'game':
        screen.blit(bg1, (0, 0))
        screen.blit(bg2, (0, 0))
        screen.blit(bg3, (0, 0))
        level.run()
        display.run()
    elif status == 'menu':
        menu.run(50, 350, 165)
    pygame.display.flip()
    clock.tick(144)
pygame.quit()
