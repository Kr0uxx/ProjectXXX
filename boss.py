import pygame
from mob import Mob


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics\\boss\\idle\\frame-001.png')
        self.image = pygame.transform.scale(self.image, (300, 202))
        self.rect = self.image.get_rect(topleft=pos)
        self.v = 7

    def move(self, player):
        self.rect.x += self.v * abs(player.rect.x - self.rect.x) / (player.rect.x - self.rect.x)

    def update(self, shift, player):
        self.move(player)
