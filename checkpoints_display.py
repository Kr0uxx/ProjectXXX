import pygame


class PointsDisplay:
    def __init__(self, screen):
        self.window = pygame.Surface((1000, 1080))
        self.points_display = []
        self.coordinates = []
        self._current_option_index = 0
        self.screen = screen

    def append_option(self, point_number, teleport):
        self.points_display.append(pygame.font.Font('dialogs\\fonts\\Bento.otf', 100).render(point_number, True,
                                                                                             (255, 255, 255)))
        self.coordinates.append(teleport)

    def switch(self, direction):
        # тут будет звук свича
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self.points_display) - 1))

    def run(self, x, y, point_y_padding):
        self.screen.blit(self.window, (0, 0))
        for j, point in enumerate(self.points_display):
            point_rect: pygame.Rect = point.get_rect()
            point_rect.topleft = (x, y + j * point_y_padding)
            if j == self._current_option_index:
                pygame.draw.rect(self.screen, (73, 74, 73), point_rect)
            self.screen.blit(point, point_rect)
