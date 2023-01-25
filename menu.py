import pygame

global status
global running


class Menu:
    def __init__(self, screen):
        self._options = []
        self._callbacks = []
        self._current_option_index = 0
        self.image = pygame.Surface((1280, 1080))
        self.screen = screen
        self.image.fill('black')

    def append_option(self, option, callback):
        self._options.append(pygame.font.SysFont('arial', 140).render(option, True, (255, 255, 255)))
        self._callbacks.append(callback)

    def switch(self, direction):
        # тут будет звук свича
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._options) - 1))

    def select(self):
        # тут будет звук селекта
        self._callbacks[self._current_option_index]()

    def run(self, x, y, option_y_padding):
        self.screen.blit(self.image, (0, 0))
        for j, option in enumerate(self._options):
            option_rect: pygame.Rect = option.get_rect()
            option_rect.topleft = (x, y + j * option_y_padding)
            if j == self._current_option_index:
                pygame.draw.rect(self.screen, (73, 74, 73), option_rect)
            self.screen.blit(option, option_rect)
