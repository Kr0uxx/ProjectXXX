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
        self.dialog_hash = 0
        self.current_dialog = 1

    def interaction(self, replicas):
        dialog = Dialog(self.screen)
        dialog.play(str(self.dialog_hash) + '0' + str(self.current_dialog), replicas)
        self.current_dialog += 1

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

    def update(self, shift):
        self.rect.x += shift
