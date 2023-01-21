import pygame
from player import Player

map1 = open("graphics/map1.txt").readlines()
size_x = 50


class Money(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("orange")

    def update(self, shift):
        # сдвиг монеток при движении камеры
        self.rect.x += shift


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("black")

    def update(self, shift):
        # сдвиг платформ при движении камеры
        self.rect.x += shift


class Level:
    def __init__(self, map, surface):
        self.surface = surface
        self.read(map)
        self.camera = 0

    def read(self, map):
        self.platforms = pygame.sprite.Group()
        self.moneys = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for ind_r, r in enumerate(map):
            for ind_c, c in enumerate(r):
                if c == "X":
                    platform = Platform((size_x * ind_c, size_x * ind_r), size_x)
                    self.platforms.add(platform)
                elif c == "P":
                    player = Player((size_x * ind_c, size_x * ind_r))
                    self.player.add(player)
                elif c == "M":
                    money = Money((size_x * ind_c, size_x * ind_r))
                    self.moneys.add(money)

    def camera_level(self):
        player = self.player.sprite
        playerx = player.rect.centerx
        playery = player.rect.centery
        vectorx = player.vector.x
        vectory = player.vector.y
        if playerx < 200 and vectorx < 0:
            self.camera = 5
            player.v = 0
        elif playerx > 600 and vectorx > 0:
            self.camera = -5
            player.v = 0
        else:
            self.camera = 0
            player.v = 5

    def vertical(self):
        player = self.player.sprite
        player.rect.x += player.vector.x * player.v
        for platform in self.platforms.sprites():
            if platform.rect.colliderect(player.rect):
                if player.vector.x > 0:
                    player.rect.right = platform.rect.left
                elif player.vector.x < 0:
                    player.rect.left = platform.rect.right

    def horizontal(self):
        player = self.player.sprite
        player.with_gravity()
        for platform in self.platforms.sprites():
            if platform.rect.colliderect(player.rect):
                if player.vector.y > 0:
                    player.vector.y = 0
                    player.rect.bottom = platform.rect.top
                elif player.vector.y < 0:
                    player.rect.top = platform.rect.bottom
                    player.vector.y = 0

    def run(self):
        self.platforms.update(self.camera)
        self.platforms.draw(self.surface)
        self.moneys.update(self.camera)
        self.moneys.draw(self.surface)
        self.camera_level()
        self.player.update()
        self.vertical()
        self.horizontal()
        self.player.draw(self.surface)
