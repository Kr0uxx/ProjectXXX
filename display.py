import pygame


class Display:
    def __init__(self, screen, width, height, hp_percent, mana_percent):
        self.hp_percent = hp_percent
        self.mana_percent = mana_percent
        self.width_hp, self.height_hp = 250 * self.hp_percent * 0.01, 30
        self.width_mana, self.height_mana = 250 * self.mana_percent * 0.01, 30
        self.width = width
        self.screen = screen
        self.bar_img = pygame.image.load("graphics\\display\\bar.png")
        self.bar_img = pygame.transform.scale(self.bar_img, (300, 100))

    def hp_subtraction(self, damage):
        self.hp_percent -= damage * 0.001
        self.width_hp = self.width * 0.168 * self.hp_percent

    def run(self):
        pygame.draw.rect(self.screen, (51, 51, 51),
                         (23, 10, 250, self.height_hp))
        pygame.draw.rect(self.screen, (51, 51, 51),
                         (23, 68, 250, self.height_mana))
        pygame.draw.rect(self.screen, (176, 0, 33),
                         (23, 10, self.width_hp, self.height_hp))
        pygame.draw.rect(self.screen, (0, 120, 176),
                         (23, 68, self.width_mana, self.height_mana))
        self.screen.blit(self.bar_img, (3, 3))
