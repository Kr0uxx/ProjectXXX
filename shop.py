import pygame
from NPC import NPC
from dialogs import Dialog


class Shop(NPC):
    def __init__(self, pos, screen):
        super().__init__(pos, screen)
        self.image = pygame.Surface((250, 250))
        self.dialog_hash = 2
        self.images = [pygame.image.load(f'graphics\\Characters\\Shop\\frame-0{i + 1}.png') for i in range(6)]
        self.animate_npc(self.images, 6, False, (250, 250))

    def interaction(self, replicas):
        dialog = Dialog(self.screen)
        dialog.play(str(self.dialog_hash) + '01', replicas)

    # def display(self):

