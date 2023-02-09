import pygame
from dialogs import Dialog


class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((30, 30))
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.rect = self.image.get_rect(topleft=pos)
        self.vector = pygame.math.Vector2(0, 0)
        self.active_dialog = 0

    def interaction(self):
        dialog = Dialog(self.screen)
        dialog.play(str(self.active_dialog) + '01', 1)

    def update(self, shift):
        self.rect.x += shift
