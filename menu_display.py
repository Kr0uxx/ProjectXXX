import pygame


class MenuDisplay:
    def __init__(self, screen):
        self._options = []
        self._callbacks = []
        self._current_option_index = 0
        self.image = pygame.Surface((1920, 1080))
        self.screen = screen
        self.image.fill('black')
        self.f = pygame.font.Font('dialogs\\fonts\\header_font.ttf', 150)
        self.text1 = self.f.render('CHICK', True, (255, 255, 255))
        self.text2 = self.f.render('ANTHOLOGY', True, (181, 20, 49))
        self.f_shadow = pygame.font.Font('dialogs\\fonts\\header_font.ttf', 158)
        self.text_shadow1 = self.f_shadow.render('CHICK', True, (0, 0, 0))
        self.text_shadow2 = self.f_shadow.render('ANTHOLOGY', True, (0, 0, 0))

    def append_option(self, option, callback):
        self._options.append(pygame.font.SysFont('arial', 140).render(option, True, (255, 255, 255)))
        self._callbacks.append(callback)

    def switch(self, direction):
        # тут будет звук свича
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._options) - 1))

    def select(self):
        pygame.mixer.Sound('music\\sounds\\select.mp3').play()
        self._callbacks[self._current_option_index]()

    def run(self, x, y, option_y_padding):
        self.screen.blit(self.image, (0, 0))
        self.screen.blit(self.text_shadow1, (732, 10))
        self.screen.blit(self.text1, (734, 20))
        self.screen.blit(self.text_shadow2, (582, 140))
        self.screen.blit(self.text2, (584, 150))
        for j, option in enumerate(self._options):
            option_rect: pygame.Rect = option.get_rect()
            option_rect.topleft = (x, y + j * option_y_padding)
            if j == self._current_option_index:
                pygame.draw.rect(self.screen, (245, 247, 225), option_rect)
            self.screen.blit(option, option_rect)

