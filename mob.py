import pygame
from random import randint


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.cur_frame = 0
        self.delay = 0
        self.flip = False
        self.images = [pygame.transform.scale(pygame.image.load(f'graphics\\mobs\\demon\\mob-{i + 1}.png'), (100, 100))
                       for i in range(8)]
        self.rect = self.images[0].get_rect(topleft=pos)
        self.vector = pygame.math.Vector2(0, 0)
        self.v = 3
        self.health = 25
        self.x_pos = self.rect.x
        self.step_counter = self.rect.x
        self.enable_movement = False
        self.gravity = 0.3
        self.attack_delay = 0
        self.lever_attack = False
        self.damage = 100

    def update(self, shift):
        self.rect.x += shift

    def with_gravity(self):
        self.vector.y += self.gravity
        self.rect.y += self.vector.y
        
    def animate_mob(self, sheet, num, size, flip):
        if self.delay == 2:
            self.cur_frame = (self.cur_frame + 1) % num
            self.delay = 0
        else:
            self.delay += 1
        self.image = sheet[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (size[0], size[1]))
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey((255, 255, 255))
