import pygame
from dialogs import Dialog


class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__()
        self.delay = 0
        self.cur_frame = 0
        self.screen = screen
        self.image = pygame.Surface((30, 30))
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.rect = self.image.get_rect(topleft=pos)
        self.vector = pygame.math.Vector2(0, 0)
        self.active_dialog = 0

    def interaction(self):
        dialog = Dialog(self.screen)
        dialog.play(str(self.active_dialog) + '01', 1)

    def update(self, shift):
        self.rect.x += shift

    def animate_npc(self, sheet, num, flip, size):
        if self.delay == 2:
            self.cur_frame = (self.cur_frame + 1) % num
            self.delay = 0
        else:
            self.delay += 1
        self.image = sheet[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (size[0], size[1]))
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey((255, 255, 255))
