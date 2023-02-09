import pygame
from NPC import NPC


class Shop(NPC):
    def __init__(self, pos, screen):
        super().__init__(pos, screen)
        self.image = pygame.image.load('graphics\\Characters\\Shop\\shop.png')
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.active_dialog = 2

    # def display(self):

