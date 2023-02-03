import pygame
from dead_screen import DeadScreen

map1 = open("maps/map1.txt").readlines()
size_x = 50
width = 1500
height = len(map1) * size_x
size = width, height
screen = pygame.display.set_mode(size)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics\\Characters\\Hero\\idle\\frame-01.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=pos)

        self.vector = pygame.math.Vector2(0, 0)
        self.v = 10
        # характеристики прыжка
        self.gravity = 1
        self.v_jump = -16

    def get_key(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.vector.x = 1
        elif keys[pygame.K_a]:
            self.vector.x = -1
        else:
            self.vector.x = 0
        if keys[pygame.K_SPACE]:
            self.jump()

    def with_gravity(self):
        self.vector.y += self.gravity
        self.rect.y += self.vector.y

    def jump(self):
        self.vector.y = self.v_jump

    def update(self):
        self.get_key()


class PlayerStats:
    def __init__(self, status, hp, mana, damage):
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
