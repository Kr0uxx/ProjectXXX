import pygame


class Shop:
    def __init__(self):
        self.font = pygame.font.Font(None, 50)
        self.text = self.font.render("Shop", True, (255, 255, 255))
        text_x = width // 2 - text.get_width() // 2
        text_y = text.get_height() // 2