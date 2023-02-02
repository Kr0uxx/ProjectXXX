import pygame
from player import Player, PlayerStats
from checkpoints_display import PointsDisplay

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
        self.active_file = 'system files/active_checkpoint'
        self.list_file = 'system files/checkpoints_list'
        self.active_point = open(self.active_file).read()
        self.points_list = open(self.list_file).read()
        self.e_key_image = pygame.image.load('graphics\\display\\keys\\e_key.png')
        self.e_key_image = pygame.transform.scale(self.e_key_image, (50, 50))
        self.display = PointsDisplay(screen)

    def teleport(self, pos):
        Player.rect.x = pos[0]
        Player.rect.y = pos[1]

    def set_point(self):
        with open("system files/active_checkpoint", "wt", encoding="utf8") as to_active_point, open(
                "system files/checkpoints_list", "wt", encoding="utf8") as to_points_list:
            to_points_list.write(self.points_list + checkpoints[self.pos] + ' ')
            self.display.append_option(checkpoints[self.pos], self.teleport(self.pos))
            to_active_point.write(checkpoints[self.pos] + ' ')

    def get_point(self):
        with open("system files/active_checkpoint", "wt", encoding="utf8") as to_active_point:
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
