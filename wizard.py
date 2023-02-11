import pygame
from NPC import NPC


class Wizard(NPC):
    def __init__(self, pos, screen):
        super().__init__(pos, screen)
        self.image = pygame.Surface((250, 250))
        self.dialog_hash = 1
        self.current_dialog = 1
        self.images = [pygame.image.load(f'graphics\\Characters\\wizard\\frame-{i + 1}.png') for i in range(14)]
        self.animate_npc(self.images, 6, False, (250, 300))


