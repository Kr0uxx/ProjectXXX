import pygame


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics\\mobs\\demon\\idle\\frame-01.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=pos)
        self.vector = pygame.math.Vector2(0, 0)
        self.v = 4
        self.x_pos = self.rect.x
        self.step_counter = self.rect.x

    def update(self, shift):
        self.rect.x += shift
