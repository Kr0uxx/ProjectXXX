import pygame


class Shop(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics\\Characters\\Shop\\shop.png')
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.rect = self.image.get_rect(topleft=pos)
        self.vector = pygame.math.Vector2(0, 0)
        self.v = 5

    def update(self, shift):
        self.rect.x += shift
