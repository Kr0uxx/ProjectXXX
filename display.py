import pygame

locations = {
    'town': 'City of the sun',
    'village': 'Village of Green Hills'
}


class Display:
    def __init__(self, screen, width, hp, mana):
        self.max_hp = hp
        self.max_mana = mana
        self.hp_percent = 100
        self.mana_percent = 100
        self.width_hp, self.height_hp = 239 * self.hp_percent * 0.01, 30
        self.width_mana, self.height_mana = 239 * self.mana_percent * 0.01, 30
        self.width = width
        self.screen = screen
        self.bar_img = pygame.image.load("graphics\\display\\bar.png")
        self.bar_img = pygame.transform.scale(self.bar_img, (300, 100))
        self.location_panel = pygame.image.load("graphics\\display\\TitlePanel02.png")
        self.location_panel = pygame.transform.scale(self.location_panel, (300, 40))
        self.f = pygame.font.Font('dialogs\\fonts\\DungeonFont.ttf', 30)
        self.text = self.f.render('City of the sun', True, (255, 255, 255))

    def hp_subtraction(self, damage):
        self.hp_percent -= damage * 100 / self.max_hp
        self.width_hp = 239 * self.hp_percent * 0.01

    def mana_subtraction(self, cost):
        self.mana_percent -= cost * 100 / self.max_mana
        self.width_hp = 239 * self.mana_percent * 0.01

    def run(self):
        pygame.draw.rect(self.screen, (51, 51, 51),
                         (23, 10, 250, self.height_hp))
        pygame.draw.rect(self.screen, (51, 51, 51),
                         (23, 68, 250, self.height_mana))
        pygame.draw.rect(self.screen, (176, 0, 33),
                         (34, 10, self.width_hp, self.height_hp))
        pygame.draw.rect(self.screen, (0, 120, 176),
                         (34, 68, self.width_mana, self.height_mana))
        self.screen.blit(self.bar_img, (3, 3))
        self.screen.blit(self.location_panel, (3, 120))
        self.screen.blit(self.text, (60, 125))
