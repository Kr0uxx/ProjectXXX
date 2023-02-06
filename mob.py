import pygame


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.gravity = 0.3
        self.image = pygame.image.load('graphics\\mobs\\demon\\idle\\frame-01.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=pos)
        self.vector = pygame.math.Vector2(0, 0)
        self.v = 3
        self.x_pos = self.rect.x
        self.step_counter = self.rect.x
        self.enable_movement = False
        self.health = 10

    def update(self, shift):
        self.rect.x += shift
    
    def with_gravity(self):
        self.vector.y += self.gravity
        self.rect.y += self.vector.y