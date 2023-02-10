import pygame
from NPC import NPC


class Shop(NPC):
    def __init__(self, pos, screen):
        super().__init__(pos, screen)
        self.image = pygame.Surface((250, 250))
        self.active_dialog = 2
        self.images = [pygame.image.load(f'graphics\\Characters\\Shop\\shop_frame{i}.png') for i in range(6)]
        self.animate_npc(self.images, 6, False, (250, 250))

    # def display(self):

