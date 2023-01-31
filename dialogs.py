import pygame
from time import sleep

characters = {
    'H\n': ['graphics\\portraits\\HeroPortrait.png'],
}


def dialogs(screen, txt):
    portrait = pygame.image.load(characters['H\n'][0])
    portrait = pygame.transform.scale(portrait, (190, 190))
    window = pygame.image.load('graphics\\display\\portrait window1.png')
    window = pygame.transform.scale(window, (210, 210))
    image = pygame.image.load("graphics\\display\\dialogue window.png")
    image = pygame.transform.scale(image, (940, 270))
    text_font = pygame.font.Font('dialogs\\fonts\\Silver.ttf', 30)
    name_font = pygame.font.Font('dialogs\\fonts\\Silver.ttf', 50)
    text = open(txt).readlines()
    county = 0
    for i in range(len(text)):
        county += 1
        countx = 0
        for j in text[i][:-1]:
            countx += 1
            write = text_font.render(j, True, (255, 255, 255))
            screen.blit(image, (30, 700))
            screen.blit(window, (60, 730))
            screen.blit(portrait, (72, 742))
            image.blit(write, (270 + 15 * countx, 40 + county * 30))
            pygame.display.flip()
            sleep(0.13)
