from pygame import font, display
from time import sleep


def dialogs(screen, text):
    text_font = font.Font('dialogs\\fonts\\erin.ttf', 30)
    screen.fill('black')
    text = open(text).readlines()
    county = 0
    for i in text:
        county += 1
        countx = 0
        for j in i[:-1]:
            countx += 1
            write = text_font.render(j, True, 'white')
            screen.blit(write, (0 + 20 * countx, 0 + county * 40))
            display.flip()
            sleep(0.18)

