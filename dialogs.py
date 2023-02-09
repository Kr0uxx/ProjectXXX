import pygame
from time import sleep

characters = {
    'H\n': ['graphics\\portraits\\HeroPortrait.png', 'Hero'],
    'W\n': ['graphics\\portraits\\Witcher.png', 'Феривий'],
    'S\n': ['graphics\\portraits\\Shop.png', 'Продавец наркоты'],
}


class Dialog:
    def __init__(self, screen):
        self.window = pygame.image.load('graphics\\display\\portrait window1.png')
        self.window = pygame.transform.scale(self.window, (210, 210))
        self.image = pygame.image.load("graphics\\display\\dialogue window.png")
        self.image = pygame.transform.scale(self.image, (1440, 270))
        self.text_font = pygame.font.Font('dialogs\\fonts\\Silver.ttf', 30)
        self.name_font = pygame.font.Font('dialogs\\fonts\\Silver.ttf', 50)
        self.county = 0
        self.screen = screen
        self.path = ''
        self.lever = False
        self.replicas = 0

    def load_dialog(self, dialog):
        return f'dialogs\\dialog-{dialog}\\replica-'

    # функция для перехода к следующей реплике по нажатию клавиши, не работает обработка
    def get_key(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.lever = False
            self.replicas += 1

    def play(self, dialog, replica_count):
        self.replicas = 1
        while self.replicas <= replica_count:
            self.screen.blit(self.image, (30, 760))
            self.screen.blit(self.window, (60, 790))

            self.county = 0
            if not self.lever:
                self.path = self.load_dialog(dialog) + '10' + str(self.replicas)
                text = open(self.path).readlines()
                portrait = pygame.image.load(characters[text[0]][0])
                portrait = pygame.transform.scale(portrait, (190, 190))
                name_write = self.name_font.render(characters[text[0]][1], False, (255, 255, 255))
                self.screen.blit(name_write, (285, 780))
                for i in range(1, len(text)):
                    self.county += 1
                    countx = 0
                    for j in text[i][:-1]:
                        countx += 1
                        write = self.text_font.render(j, True, (255, 255, 255))
                        self.screen.blit(portrait, (72, 802))
                        self.screen.blit(write, (300 + 15 * countx, 800 + self.county * 30))
                        pygame.display.flip()
                        sleep(0.08)
                self.lever = True
                sleep(2)
            else:
                self.lever = False
                self.replicas += 1