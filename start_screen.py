import pygame

global status
global running


class StartScreen:
    def __init__(self, screen, width):
        self._options = []
        self._callbacks = []
        self._current_option_index = 0
        self.layer0 = pygame.image.load("graphics\\Layer_0011_0.png")
        self.layer0 = pygame.transform.scale(self.layer0, (width, 1380))
        self.layer1 = pygame.image.load("graphics\\Layer_0010_1.png")
        self.layer1 = pygame.transform.scale(self.layer1, (width, 1380))
        self.layer2 = pygame.image.load("graphics\\Layer_0009_2.png")
        self.layer2 = pygame.transform.scale(self.layer2, (width, 1380))
        self.layer3 = pygame.image.load("graphics\\Layer_0008_3.png")
        self.layer3 = pygame.transform.scale(self.layer3, (width, 1380))
        self.layer4 = pygame.image.load("graphics\\Layer_0007_Lights.png")
        self.layer4 = pygame.transform.scale(self.layer4, (width, 1380))
        self.layer5 = pygame.image.load("graphics\\Layer_0006_4.png")
        self.layer5 = pygame.transform.scale(self.layer5, (width, 1380))
        self.layer6 = pygame.image.load("graphics\\Layer_0005_5.png")
        self.layer6 = pygame.transform.scale(self.layer6, (width, 1380))
        self.layer7 = pygame.image.load("graphics\\Layer_0004_Lights.png")
        self.layer7 = pygame.transform.scale(self.layer7, (width, 1380))
        self.layer8 = pygame.image.load("graphics\\Layer_0003_6.png")
        self.layer8 = pygame.transform.scale(self.layer8, (width, 1380))
        self.layer9 = pygame.image.load("graphics\\Layer_0002_7.png")
        self.layer9 = pygame.transform.scale(self.layer9, (width, 1380))
        self.layer10 = pygame.image.load("graphics\\Layer_0001_8.png")
        self.layer10 = pygame.transform.scale(self.layer10, (width, 1380))
        self.layer11 = pygame.image.load("graphics\\Layer_0000_9.png")
        self.layer11 = pygame.transform.scale(self.layer11, (width, 1380))
        self.music = 'music\\main theme.mp3'
        self.screen = screen

    def append_option(self, option, callback):
        self._options.append(pygame.font.Font('dialogs\\fonts\\Bento.otf', 100).render(option, True, (255, 255, 255)))
        self._callbacks.append(callback)

    def switch(self, direction):
        # тут будет звук свича
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._options) - 1))

    def select(self):
        pygame.mixer.Sound('music\\sounds\\select.mp3').play()
        self._callbacks[self._current_option_index]()

    def run(self, x, y, option_y_padding):
        self.screen.blit(self.layer0, (0, -300))
        self.screen.blit(self.layer1, (0, -300))
        self.screen.blit(self.layer2, (0, -300))
        self.screen.blit(self.layer3, (0, -300))
        self.screen.blit(self.layer4, (0, -300))
        self.screen.blit(self.layer5, (0, -300))
        self.screen.blit(self.layer6, (0, -300))
        self.screen.blit(self.layer7, (0, -300))
        self.screen.blit(self.layer8, (0, -300))
        self.screen.blit(self.layer9, (0, -300))
        self.screen.blit(self.layer10, (0, -300))
        self.screen.blit(self.layer11, (0, -300))
        for j, option in enumerate(self._options):
            option_rect: pygame.Rect = option.get_rect()
            option_rect.topleft = (x, y + j * option_y_padding)
            if j == self._current_option_index:
                pygame.draw.rect(self.screen, (73, 74, 73), option_rect)
            self.screen.blit(option, option_rect)
