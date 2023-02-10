import pygame
from dead_screen import DeadScreen

map1 = open("maps/map1.txt").readlines()
size_x = 50
width = 1000
height = len(map1) * size_x
size = width, height
screen = pygame.display.set_mode(size)
player_v = 10


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.idle_images = []
        for i in range(6):
            self.idle_images.append(pygame.image.load(f'graphics\\Characters\\Hero\\idle\\ChikIdle\\ChikIdle_frame{i}.png'))
        self.rect = pygame.image.load('graphics\\Characters\\Hero\\idle\\ChikIdle\\ChikIdle_frame0.png').get_rect(topleft=pos)
        self.rect[2] = 50
        self.rect[3] = 100
        self.run_images = []
        for i in range(10):
            self.run_images.append(pygame.image.load(f'graphics\\Characters\\Hero\\idle\\ChikRun\\ChikRun_frame{i}.png'))
        self.direction = 1
        self.platforms = pygame.sprite.Group()
        self.plat_rects = [platform.rect for platform in self.platforms]
        self.vector = pygame.math.Vector2(0, 0)
        self.v = player_v
        # характеристики прыжка
        self.gravity = 0.3
        self.v_jump = -5
        self.damage = 5
        # self.attack_effect = Effect((pos[0] + 20, pos[1] + 20), 'graphics\\effects\\attack effects\\SFX301_', 5)
        # self.rect = self.attack_image.get_rect(topleft=pos)
        # self.attack_images = []
        # for i in range(5):
        #     self.attack_images.append(
        #         pygame.transform.scale(pygame.image.load(f'graphics\\effects\\attack effects\\SFX301_frame{i}.png'), (30, 30)))
        self.cur_frame = 0
        self.delay = 0
        self.prev_vector = False
        self.status = 'stand'
        self.effect = pygame.sprite.GroupSingle
        self.animate(self.idle_images, 6, False)

    def animate(self, sheet, num, flip):
        if self.delay == 3:
            self.cur_frame = (self.cur_frame + 1) % num
            self.delay = 0
        else:
            self.delay += 1
        self.image = sheet[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (50, 100))
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey((255, 255, 255))

    def move(self):
        keys = pygame.key.get_pressed()
        print(self.status)
        if pygame.sprite.spritecollideany(self, self.platforms):
            self.status = 'jump'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if not self.vector.x:
                self.cur_frame = 0
            self.vector.x = 1
            self.direction = 1
            if self.status != 'jump':
                self.animate(self.run_images, 10, False)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not self.vector.x:
                self.cur_frame = 0
            self.vector.x = -1
            self.direction = 0
            if self.status != 'jump':
                self.animate(self.run_images, 10, True)
        else:
            if self.vector.x == -1:
                self.prev_vector = True
                self.cur_frame = 0
            if self.vector.x == 1:
                self.prev_vector = False
                self.cur_frame = 0
            self.vector.x = 0
            if self.status != 'jump':
                self.animate(self.idle_images, 6, self.prev_vector)

    def attack(self, mob):
        mob.health -= self.damage
        print("enemy health:", mob.health)

    def with_gravity(self):
        self.vector.y += self.gravity
        self.rect.y += self.vector.y

    def jump(self):
        self.vector.y = self.v_jump

    def update(self):
        self.move()


class Collision(Player):
    def __init__(self, pos, player):
        super().__init__(pos)
        self.width = 200
        self.height = player.rect[3]
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("grey")
        # self.vector = pygame.math.Vector2(0, 0)

    def update(self, player):
        if not player.direction:
            self.rect.x = player.rect.x + player.rect[2] - self.width
            self.rect.y = player.rect.y
        else:
            self.rect.x = player.rect.x
            self.rect.y = player.rect.y


class Effect(Player):
    def __init__(self, pos):
        super().__init__(pos)
        self.cur_frame = 0
        self.delay = 0
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(topleft=pos)
        self.images = []

    def update(self, player):
        if not player.direction:
            self.rect.x = player.rect.x + player.rect[2] - 100
            self.rect.y = player.rect.y + 15
        else:
            self.rect.x = player.rect.x + 40
            self.rect.y = player.rect.y + 15

    def animate_effect(self, sheet, num, flip):
        self.images = [pygame.image.load(f'{sheet}_frame{i}.png') for i in range(num)]
        self.cur_frame = (self.cur_frame + 1) % num
        self.image = self.images[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (50, 100))
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey((255, 255, 255))


class PlayerStats:
    def __init__(self, status, hp, mana,  damage):
        self.status = status
        self.max_hp = hp
        self.max_mana = mana
        self.hp = hp
        self.mana = mana
        self.damage = damage

    def get_damage(self, damage):
        if (self.hp <= damage or self.hp < 1) and self.status != 'death':
            self.status = 'death'
            pygame.mixer.Sound('music\\sounds\\death music.mp3').play()
        elif self.hp > 0:
            self.hp -= damage