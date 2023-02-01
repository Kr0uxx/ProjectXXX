import pygame
from player import Player, PlayerStats

checkpoints = {(600, 450): '1',
               (2800, 500): '2'}


class CheckPoint(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__()
        self.image = pygame.image.load('graphics\\checkpoint\\frame-01.png')
        self.image = pygame.transform.scale(self.image, (100, 290))
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.vector = pygame.math.Vector2(0, 0)
        self.v = 5
        self.active_file = 'graphics\\checkpoint\\active_checkpoint'
        self.list_file = 'graphics\\checkpoint\\checkpoints_list'
        self.active_point = open(self.active_file).read()
        self.points_list = open(self.list_file).read()
        self.e_key_image = pygame.image.load('graphics\\display\\keys\\e_key.png')
        self.e_key_image = pygame.transform.scale(self.e_key_image, (50, 50))
        self.display = PointsDisplay(screen)

    def teleport(self, pos):
        Player.rect.x = pos[0]
        Player.rect.y = pos[1]

    def set_point(self):
        with open("graphics\\checkpoint\\active_checkpoint", "wt", encoding="utf8") as to_active_point, open(
                "graphics\\checkpoint\\checkpoints_list", "wt", encoding="utf8") as to_points_list:
            to_points_list.write(self.points_list + checkpoints[self.pos] + ' ')
            self.display.append_option(checkpoints[self.pos], self.teleport(self.pos))
            to_active_point.write(checkpoints[self.pos] + ' ')

    def get_point(self):
        with open("graphics\\checkpoint\\active_checkpoint", "wt", encoding="utf8") as to_active_point:
            to_active_point.write(checkpoints[self.pos] + ' ')

    def is_point_checking(self):
        if checkpoints[self.pos] in self.points_list.split():
            return True
        return False

    def interaction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            if self.is_point_checking():
                self.get_point()
            else:
                self.set_point()
            self.display.run(50, 350, 165)

    def update(self, shift):
        self.rect.x += shift


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
