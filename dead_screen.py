import pygame


class DeadScreen:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.Surface((1280, 1080))
        self.image.fill('black')

    def run(self):
        self.screen.blit(self.image, (0, 0))
        f = pygame.font.SysFont('Serif', 200)
        text = f.render('YOU DIED', True, (84, 46, 42))
        self.screen.blit(text, (20, 250))
