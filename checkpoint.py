import pygame
from checkpoints_display import PointsDisplay

checkpoints = {(600, 450): '1',
               (3500, 500): '2'}


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
        self.points_display = PointsDisplay(screen)

    def set_point(self):
        with open("system files/active_checkpoint", "wt", encoding="utf8") as to_active_point, open(
                "system files/checkpoints_list", "wt", encoding="utf8") as to_points_list:
            to_points_list.write(self.points_list + checkpoints[self.pos] + ' ')
            to_active_point.write(checkpoints[self.pos] + ' ')

    def get_point(self):
        with open("system files/active_checkpoint", "wt", encoding="utf8") as to_active_point:
            to_active_point.write(checkpoints[self.pos] + ' ')

    def is_point_checking(self):
        if checkpoints[self.pos] in self.points_list.split():
            return True
        return False

    def interaction(self):
        if self.is_point_checking():
            self.get_point()
        else:
            self.set_point()
        return True

    def update(self, shift):
        self.rect.x += shift
