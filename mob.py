import pygame


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=pos)
        self.vector = pygame.math.Vector2(0, 0)
        self.v = 5

    def update(self, shift):
        self.rect.x += shift
