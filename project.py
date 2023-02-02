import pygame
import time
from level import Level
from display import Display
from menu import Menu
from start_screen import StartScreen
from dead_screen import DeadScreen
from player import PlayerStats
from dialogs import dialogs
from checkpoints_display import PointsDisplay

pygame.init()
running = True

''' 6 состояний: game - в игре, start - на начальном экране, menu - в меню, death - на экране смерти, dialog - диалог, 
 point - точка сохранения'''
status = 'start'

# карта для уровня
map1 = open("maps/map1.txt").readlines()
active_map = map1

# музыка
main_theme = 'music\\main theme.mp3'
start_screen_theme = 'music\\start screen theme.mp3'


def music(music_name, volume=0.5, loops=-1):
    pygame.mixer.music.load(music_name)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops=loops)


music(start_screen_theme)
size_x = 50
width = 1000
height = len(map1) * size_x
damage = 5

size = width, height
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

level = Level(map1, screen)

player_stats = PlayerStats(status, 1000, 1000, damage)
display = Display(screen, width, player_stats.hp, player_stats.mana)


# f меню:

def quit_game():
    global running
    running = False


def resume_game():
    music(main_theme)
    player_stats.status = 'game'


def start_game():
    player_stats.status = 'game'


def load_game():
    player_stats.status = 'game'


def go_start_screen():
    player_stats.status = 'start'


def open_settings():
    pass


# меню
menu = Menu(screen)
menu.append_option('Resume', resume_game)
menu.append_option('Settings', open_settings)
menu.append_option('Start Screen', go_start_screen)
menu.append_option('Quit', quit_game)

# начальный экран
start_screen = StartScreen(screen)
start_screen.append_option('Start', resume_game)
start_screen.append_option('Settings', open_settings)
start_screen.append_option('Quit', quit_game)

# экран смерти
dead_screen = DeadScreen(screen)

# графика
bg1 = pygame.image.load("graphics\\background_layer_1.png")
bg1 = pygame.transform.scale(bg1, (1000, 1080))
bg2 = pygame.image.load("graphics\\background_layer_2.png")
bg2 = pygame.transform.scale(bg2, (1000, 1080))
bg3 = pygame.image.load("graphics\\background_layer_3.png")
bg3 = pygame.transform.scale(bg3, (1000, 1080))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if player_stats.status == 'game':
                if event.key == pygame.K_ESCAPE:
                    player_stats.status = 'menu'
            elif player_stats.status == 'start':
                if event.key == pygame.K_w:
                    start_screen.switch(-1)
                elif event.key == pygame.K_s:
                    start_screen.switch(1)
                elif event.key == pygame.K_RETURN:
                    start_screen.select()
            elif player_stats.status == 'menu':
                if event.key == pygame.K_w:
                    menu.switch(-1)
                elif event.key == pygame.K_s:
                    menu.switch(1)
                elif event.key == pygame.K_RETURN:
                    menu.select()
            if event.key == pygame.K_y:
                player_stats.get_damage(10)
                display.hp_subtraction(10)
            if event.key == pygame.K_q:
                player_stats.status = 'dialog'
    if player_stats.status == 'death':
        pygame.mixer.music.stop()
        dead_screen.run()
    elif player_stats.status == 'game':
        screen.blit(bg1, (0, 0))
        screen.blit(bg2, (0, 0))
        screen.blit(bg3, (0, 0))
        level.run()
        display.run()
    elif player_stats.status == 'start':
        start_screen.run(50, 350, 165)
    elif player_stats.status == 'menu':
        menu.run(50, 350, 165)
    elif player_stats.status == 'dialog':
        dialogs(screen, 'dialogs\\dialog001\\dialog1')
        time.sleep(2)
        player_stats.status = 'game'
    elif player_stats.status == 'point':
        pass
    pygame.display.flip()
    clock.tick(144)
pygame.quit()
