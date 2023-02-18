import pygame
from checkpoints_display import PointsDisplay

checkpoints = {(2050, 500): '1',
               (5300, 500): '2',
               (7800, 500): '3'
               }


class CheckPoint(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__()
        self.delay = 0
        self.cur_frame = 0
        self.image = pygame.Surface((100, 290))
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.vector = pygame.math.Vector2(0, 0)
        self.v = 5
        self.active_file = 'system files/active_checkpoint'
        self.list_file = 'system files/checkpoints_list'
        self.active_point = open(self.active_file).read()
        self.points_list = open(self.list_file).read()
        self.points_display = PointsDisplay(screen)
        self.images = [pygame.image.load(f'graphics\\checkpoint\\frame-{i + 1}.png') for i in range(13)]

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

    def animate(self, sheet, num, flip):
        if self.delay == 2:
            self.cur_frame = (self.cur_frame + 1) % num
            self.delay = 0
        else:
            self.delay += 1
        self.image = sheet[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (100, 290))
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey((255, 255, 255))

    def update(self, shift):
        self.animate(self.images, 13, False)
        self.rect.x += shift
