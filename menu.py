import pygame
from menu_display import MenuDisplay


class Menu(MenuDisplay):
    def __init__(self, screen):
        super().__init__(screen)
        self.image = pygame.image.load("graphics\\menu_bg.jpg")
        self.image = pygame.transform.scale(self.image, (1920, 1080))

    def append_option(self, option, callback):
        self._options.append(pygame.font.Font('dialogs\\fonts\\Bento.otf', 100).render(option, True, (233, 211, 3)))
        self._callbacks.append(callback)
