import pygame
from random import randint


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics\\mobs\\demon\\idle\\frame-01.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=pos)
        self.vector = pygame.math.Vector2(0, 0)
        self.v = 3
        self.health = 25
        self.x_pos = self.rect.x
        self.step_counter = self.rect.x
        self.enable_movement = False
        self.gravity = 0.3
        self.attack_delay = 0
        self.lever_attack = False
        self.damage = 40

    def update(self, shift):
        self.rect.x += shift

    def with_gravity(self):
        self.vector.y += self.gravity
        self.rect.y += self.vector.y
