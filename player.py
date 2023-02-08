import pygame
from dead_screen import DeadScreen

map1 = open("maps/map1.txt").readlines()
size_x = 50
width = 1000
height = len(map1) * size_x
size = width, height
screen = pygame.display.set_mode(size)
player_v = 10


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image_idle = pygame.image.load('graphics\\Characters\\Hero\\idle\\ChikBoy_idle.png')
        self.image_idle.set_colorkey((255, 255, 255))
        self.image_idle = pygame.transform.scale(self.image_idle, (100, 600))
        self.image_run = pygame.image.load('graphics\\Characters\\Hero\\idle\\ChikBoy_run.png')
        self.image_run = pygame.transform.scale(self.image_run, (100, 1000))
        self.image_run.set_colorkey((255, 255, 255))
        self.rect = self.image_idle.get_rect(topleft=pos)
        self.direction = 1
        self.vector = pygame.math.Vector2(0, 0)
        self.v = player_v
        # характеристики прыжка
        self.gravity = 0.3
        self.v_jump = -5
        self.damage = 5
        self.cur_frame = 0
        self.delay = 0
        self.prev_vector = False
        self.animate(self.image_idle, 1, 6, self.rect.x, self.rect.y, False)

    def animate(self, sheet, columns, rows, x, y, flip):
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        if self.delay == 3:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.delay = 0
        else:
            self.delay += 1
        self.image = self.frames[self.cur_frame]
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if not self.vector.x:
                self.cur_frame = 0
            self.vector.x = 1
            self.direction = 1
            self.animate(self.image_run, 1, 10, self.rect.x, self.rect.y, False)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not self.vector.x:
                self.cur_frame = 0
            self.vector.x = -1
            self.direction = 0
            self.animate(self.image_run, 1, 10, self.rect.x, self.rect.y, True)
        else:
            if self.vector.x == -1:
                self.prev_vector = True
                self.cur_frame = 0
            if self.vector.x == 1:
                self.prev_vector = False
                self.cur_frame = 0
            self.vector.x = 0
            self.animate(self.image_idle, 1, 6, self.rect.x, self.rect.y, self.prev_vector)

    def attack(self, mob):
        mob.health -= self.damage
        print("enemy health:", mob.health)

    def with_gravity(self):
        self.vector.y += self.gravity
        self.rect.y += self.vector.y

    def jump(self):
        self.vector.y = self.v_jump

    def update(self):
        self.move()


class Collision(Player):
    def __init__(self, pos, player):
        super().__init__(pos)
        self.width = 200
        self.height = player.rect[3]
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("grey")
        # self.vector = pygame.math.Vector2(0, 0)

    def update(self, player):
        if not player.direction:
            self.rect.x = player.rect.x + player.rect[2] - self.width
            self.rect.y = player.rect.y
        else:
            self.rect.x = player.rect.x
            self.rect.y = player.rect.y


class PlayerStats:
    def __init__(self, status, hp, mana,  damage):
        self.status = status
        self.max_hp = hp
        self.max_mana = mana
        self.hp = hp
        self.mana = mana
        self.damage = damage

    def get_damage(self, damage):
        if (self.hp <= damage or self.hp < 1) and self.status != 'death':
            self.status = 'death'
            pygame.mixer.Sound('music\\sounds\\death music.mp3').play()
        elif self.hp > 0:
            self.hp -= damage