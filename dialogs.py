import pygame
from time import sleep

characters = {
    'H\n': ['graphics\\portraits\\hero_portrait.png', 'Hero'],
    'W\n': ['graphics\\portraits\\wizard.png', 'Ferivius'],
    'S\n': ['graphics\\portraits\\Shopp.png', 'Dealer'],
}


class Dialog:
    def __init__(self, screen):
        self.portrait_window = pygame.image.load('graphics\\display\\Button03.png')
        self.portrait_window = pygame.transform.scale(self.portrait_window, (180, 180))
        self.window = pygame.image.load("graphics\\display\\dialogue window2.png")
        self.window = pygame.transform.scale(self.window, (1860, 240))
        self.text_font = pygame.font.Font('dialogs\\fonts\\Silver.ttf', 30)
        self.name_font = pygame.font.Font('dialogs\\fonts\\Silver.ttf', 50)
        self.county = 0
        self.screen = screen
        self.path = ''
        self.lever = False
        self.replicas = 0
        self.sleep_time = 0.08

    def load_dialog(self, dialog):
        return f'dialogs\\dialog-{dialog}\\replica-'

    def get_key(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.lever = False
            self.replicas += 1

    def play(self, dialog, replica_count):
        self.replicas = 1
        while self.replicas <= replica_count:
            self.screen.blit(self.window, (30, 790))
            self.screen.blit(self.portrait_window, (70, 820))

            self.county = 0
            if not self.lever:
                self.path = self.load_dialog(dialog) + '10' + str(self.replicas)
                text = open(self.path).readlines()
                portrait = pygame.image.load(characters[text[0]][0])
                portrait = pygame.transform.scale(portrait, (140, 140))
                name_write = self.name_font.render(characters[text[0]][1], False, (255, 255, 255))
                self.screen.blit(name_write, (285, 810))
                for i in range(1, len(text)):
                    self.county += 1
                    countx = 0
                    for j in text[i][:-1]:
                        countx += 1
                        write = self.text_font.render(j, True, (255, 255, 255))
                        self.screen.blit(portrait, (88, 837))
                        self.screen.blit(write, (300 + 15 * countx, 830 + self.county * 30))
                        pygame.display.flip()
                        sleep(self.sleep_time)
                self.lever = True
                sleep(2)
            else:
                self.lever = False
                self.replicas += 1
