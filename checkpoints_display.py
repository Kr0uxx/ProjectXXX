import pygame

checkpoints = {(2050, 500): '1',
               (5300, 500): '2',
               (7800, 500): '3'
}

checkpoints2 = {'1': (2050, 500),
                '2': (5300, 500),
                '3': (7800, 500)
                }


class PointsDisplay:
    def __init__(self, screen):
        self.window = pygame.Surface((1920, 1080))
        self.points_display = []
        self.function = []
        self.coordinates = []
        self.current_option_index = 0
        self.screen = screen
        self.already_added = []

    def append_option(self, teleport):
        for i in sorted(open("system files/checkpoints_list").read().split()):
            if i not in self.already_added:
                self.points_display.append(pygame.font.Font('dialogs\\fonts\\Silver.ttf', 100).render(i, True,
                                                                                                      (255, 255, 255)))
                self.function.append(teleport)
                self.coordinates.append(checkpoints2[i])
                self.already_added.append(i)

    def switch(self, direction):
        # тут будет звук свича
        self.current_option_index = max(0, min(self.current_option_index + direction, len(self.points_display) - 1))

    def select(self):
        pygame.mixer.Sound('music\\sounds\\select.mp3').play()
        self.function[self.current_option_index]()

    def run(self, x, y, point_y_padding):
        self.screen.blit(self.window, (0, 0))
        for j, point in enumerate(self.points_display):
            point_rect: pygame.Rect = point.get_rect()
            point_rect.topleft = (x, y + j * point_y_padding)
            if j == self.current_option_index:
                pygame.draw.rect(self.screen, (73, 74, 73), point_rect)
            self.screen.blit(point, point_rect)
