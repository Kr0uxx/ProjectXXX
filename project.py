import pygame
import time
from level import Level
from display import Display
from menu import Menu
from start_screen import StartScreen
from dead_screen import DeadScreen
from player import PlayerStats, Player
from dialogs import Dialog
from checkpoints_display import PointsDisplay
from levels_display import LvlDisplay

pygame.init()
running = True

''' 6 состояний: game - в игре, start - на начальном экране, menu - в меню, death - на экране смерти, dialog - диалог, 
 point - точка сохранения'''
status = 'start'

# карта для уровня
map1 = open("maps/map1.txt").readlines()
map2 = open("maps/map2.txt").readlines()
map3 = open("maps/map1.txt").readlines()
map_boss = open("maps/map_boss").readlines()
active_map = map1

# музыка
main_theme = 'music\\main theme.mp3'
start_screen_theme = 'music\\start screen theme.mp3'


def music(music_name, volume=0.3, loops=-1):
    pygame.mixer.music.load(music_name)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops=loops)


music(start_screen_theme)
size_x = 50
width = 1920
height = 1080
damage = 5

size = width, height
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
clock = pygame.time.Clock()
player_stats = PlayerStats(status, 1000, 1000, damage)
level = Level(active_map, screen, player_stats.status)
location = 'village'
display = Display(screen, width, player_stats.hp, player_stats.mana)
dialog = Dialog(screen)

# игрок
player = Player(level.read(active_map))
player_sprite = pygame.sprite.GroupSingle()
player_sprite.add(player)

checkpoints = {(600, 450): '1 ',
               (3500, 500): '2 '}
checkpoints2 = {'1 ': (600, 450),
                '2 ': (3500, 500)}


def teleport():
    global player
    player = player_sprite.sprite
    x = points_display.coordinates[points_display.current_option_index][0]
    active = open('system files/active_checkpoint').read()
    minus = checkpoints2[active][0]
    y = points_display.coordinates[points_display.current_option_index][1]
    with open("system files/active_checkpoint", "wt", encoding="utf8") as to_active_point:
        to_active_point.write(checkpoints[x, y])
    x -= minus
    y += 200
    level.camera_centred(-x)
    player_stats.status = 'game'


# f меню:

def quit_game():
    global running
    running = False


def resume_game():
    pygame.mixer.music.unpause()
    player_stats.status = 'game'


def start_game():
    with open('system files/checkpoints_list', 'wb') as file:
        file.write(None)
    player_stats.status = 'game'


def load_game():
    player_stats.status = 'game'
    global player
    player = player_sprite.sprite
    active = open('system files/active_checkpoint').read()
    x, y = checkpoints2[active][0], checkpoints2[active][1] + 200
    print(x, 0 - x)
    level.camera_centred(-x)


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
start_screen = StartScreen(screen, width)
start_screen.append_option('New game', resume_game)
start_screen.append_option('Load game', load_game)
start_screen.append_option('Settings', open_settings)
start_screen.append_option('Quit', quit_game)

# экран смерти
dead_screen = DeadScreen(screen)

# экран контрольных точек
points_display = PointsDisplay(screen)

# графика
if location == 'town':
    bg1 = pygame.image.load("graphics\\background_layer_1.png")
    bg1 = pygame.transform.scale(bg1, (width, 1080))
    bg2 = pygame.image.load("graphics\\background_layer_2.png")
    bg2 = pygame.transform.scale(bg2, (width, 1080))
    bg3 = pygame.image.load("graphics\\background_layer_3.png")
    bg3 = pygame.transform.scale(bg3, (width, 1080))
else:
    bg1 = pygame.image.load("graphics\\background_layer_3.png")
    bg1 = pygame.transform.scale(bg1, (width, 1080))
    bg2 = pygame.image.load("graphics\\background_layer_2.png")
    bg2 = pygame.transform.scale(bg2, (width, 1080))
    bg3 = pygame.image.load("graphics\\bg.png")
    bg3 = pygame.transform.scale(bg3, (width, 1080))

all_sprites = pygame.sprite.Group()
cursor = pygame.sprite.Sprite(all_sprites)
cursor.image = pygame.image.load('graphics\\display\\cursor.png')
cursor.image = pygame.transform.scale(cursor.image, (20, 30))
cursor.rect = cursor.image.get_rect()
pygame.mouse.set_visible(False)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            cursor.rect.topleft = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_stats.status == 'game':
                if event.button == 1:
                    pygame.mixer.Sound('music\\sounds\\attack_sound.mp3').play()
                    level.player.sprite.status = 'attack'
                    level.enemy_hurt()
        if event.type == pygame.KEYDOWN:
            if player_stats.status == 'game':
                if event.key == pygame.K_ESCAPE:
                    player_stats.status = 'menu'
                # говнокод снизу
                if event.key == pygame.K_SPACE:
                    level.jump_check()
            if player_stats.status == 'start':
                if event.key == pygame.K_w:
                    start_screen.switch(-1)
                elif event.key == pygame.K_s:
                    start_screen.switch(1)
                elif event.key == pygame.K_RETURN:
                    start_screen.select()
            if player_stats.status == 'menu':
                if event.key == pygame.K_w:
                    menu.switch(-1)
                elif event.key == pygame.K_s:
                    menu.switch(1)
                elif event.key == pygame.K_RETURN:
                    menu.select()
            if player_stats.status == 'point':
                if event.key == pygame.K_ESCAPE:
                    player_stats.status = 'game'
                elif event.key == pygame.K_w:
                    points_display.switch(-1)
                elif event.key == pygame.K_s:
                    points_display.switch(1)
                elif event.key == pygame.K_RETURN:
                    points_display.select()
    if player_stats.status == 'death':
        pygame.mixer.music.stop()
        dead_screen.run()
    elif player_stats.status == 'dialog':
        dialog.play(101, 2)
        time.sleep(2)
        player_stats.status = 'game'
    elif player_stats.status == 'game':
        # if location.read() == 'town':
        screen.blit(bg1, (0, 0))
        screen.blit(bg2, (0, 0))
        screen.blit(bg3, (0, 0))
        '''else:
            bg1 = pygame.image.load("graphics\\bg.png")
            bg1 = pygame.transform.scale(bg1, (width, 1080))
            screen.blit(bg1, (0, 0))'''
        level.run()
        if level.open_checkpoint():
            player_stats.status = 'point'
    elif player_stats.status == 'start':
        music(start_screen_theme)
        start_screen.run(50, 350, 165)
    elif player_stats.status == 'menu':
        pygame.mixer.music.pause()
        menu.run(50, 350, 165)
    elif player_stats.status == 'point':
        points_display.run(50, 350, 165)
        points_display.append_option(teleport)
    if player_stats.status != 'game':
        if pygame.mouse.get_focused():
            all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(144)
pygame.quit()
