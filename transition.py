import pygame


class Transition(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.pos = pos


    '''def interaction(self, player):
        if self.transitions[self.pos] % 2 == 1:
            player.rect.x = self.transitions_reverse[self.transitions[self.pos] + 1][1][0]'''

    def update(self, shift):
        self.rect.x += shift
