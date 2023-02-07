import pygame

from display import Display
from player import Player, PlayerStats, Collision
from mob import Mob
from shop import Shop
from checkpoint import CheckPoint

map1 = open("maps/map1.txt").readlines()
size_x = 50
width = 1000
f = open("maps//map1.txt", mode="rt")
data = f.readlines()
map_w = len(data[17]) * size_x
height = len(data) * size_x
f.close()
status = 'start'
hp = 100
damage = 5
up_counter = 0
jump_state = False
player_v = 10
size = width, height
screen = pygame.display.set_mode(size)
player_stats = PlayerStats(status, 1000, 1000, damage)
display = Display(screen, width, player_stats.hp, player_stats.mana)


class Money(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect(topleft=pos)
        self.images = []
        for i in range(7):
            self.images.append(
                pygame.transform.scale(pygame.image.load(f'graphics\\Characters\\Hero\\idle\\coin-0{i + 1}.png'), (30, 30)))
        self.n = 0
        self.image = self.images[self.n]

    def update(self, shift):
        #прокрутка списка изображений
        self.n += 1
        if self.n >= len(self.images):
            self.n = 0
        self.image = self.images[self.n]
        #animation("money", "coin", 7, 30, 30)
        # сдвиг монеток при движении камеры
        self.rect.x += shift


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.size = size
        self.image = pygame.image.load('graphics\\tiles\\town01.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, shift):
        # сдвиг платформ при движении камеры
        self.rect.x += shift

    '''7 типов: поверхностные(X), боковые левые(L), средние(Z), боково-поверхностные левые(I), 
    боково-поверхностные правые(J), всякие(A), боковые правые(R)'''

    def type(self, typ):
        # тут лучше потом переделать хранение через словарь))
        if typ == 'X':
            self.image = pygame.image.load('graphics\\tiles\\town01.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'R':
            self.image = pygame.image.load('graphics\\tiles\\town02.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'L':
            self.image = pygame.image.load('graphics\\tiles\\town07.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'Z':
            self.image = pygame.image.load('graphics\\tiles\\town03.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'I':
            self.image = pygame.image.load('graphics\\tiles\\town04.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'J':
            self.image = pygame.image.load('graphics\\tiles\\town05.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'A':
            self.image = pygame.image.load('graphics\\tiles\\town06.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))


def cut_sheet(self, sheet, columns, rows):
    self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (self.rect.w * i, self.rect.h * j)
            self.frames.append(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))


class Level:
    def __init__(self, map2, screen, display, player_stats):
        self.screen = screen
        self.read(map2)
        self.camera = 0
        self.money = 0
        self.display = display
        self.attack_enabled = False
        self.player_stats = player_stats

    def read(self, map2):
        self.platforms = pygame.sprite.Group()
        self.moneys = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.collision = pygame.sprite.GroupSingle()
        self.mobs = pygame.sprite.Group()
        self.shops = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        for ind_r, r in enumerate(map2):
            for ind_c, c in enumerate(r):
                if c == "X" or c == "L" or c == "R" or c == "Z" or c == "I" or c == "J" or c == "A":
                    platform = Platform((size_x * ind_c, size_x * ind_r), size_x)
                    platform.type(c)
                    self.platforms.add(platform)
                elif c == "P":
                    player = Player((size_x * ind_c, size_x * ind_r))
                    self.player.add(player)
                    collision = Collision((size_x * ind_c, size_x * ind_r), self.player.sprite)
                    self.collision.add(collision)
                elif c == "M":
                    money = Money((size_x * ind_c, size_x * ind_r))
                    self.moneys.add(money)
                elif c == 'E':
                    enemy = Mob((size_x * ind_c, size_x * ind_r))
                    self.mobs.add(enemy)
                elif c == 'S':
                    shop = Shop((size_x * ind_c, size_x * ind_r))
                    self.shops.add(shop)
                elif c == 'C':
                    checkpoint = CheckPoint((size_x * ind_c, size_x * ind_r), self.screen)
                    print((size_x * ind_c, size_x * ind_r))
                    self.checkpoints.add(checkpoint)

    def camera_level(self):
        player = self.player.sprite
        playerx = player.rect.centerx
        playery = player.rect.centery
        vectorx = player.vector.x
        vectory = player.vector.y
        if playerx <= width / 2 and vectorx < 0:
            self.camera = 5
            player.v = 0
        elif playerx > width / 2 and vectorx > 0:
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

    def get_money(self):
        player = self.player.sprite
        for money in self.moneys:
            if pygame.sprite.collide_rect(money, player):
                pygame.mixer.Sound('music\\sounds\\coin.wav').play()
                money.kill()
                self.money += 1
        f = pygame.font.Font(None, 40)
        text = f.render(f"money: {str(self.money)}", True, (0, 0, 0))
        self.screen.blit(text, (20, 130))

    def enemy_death(self):
        player = self.player.sprite
        for mob in self.mobs:
            if pygame.sprite.collide_rect(mob, self.collision.sprite):
                player.attack(mob)
            if mob.health == 0:
                mob.kill()
                money = Money((mob.rect[0] + 50, mob.rect[1]))
                self.moneys.add(money)
                money = Money((mob.rect[0], mob.rect[1]))
                self.moneys.add(money)
                money = Money((mob.rect[0] - 50, mob.rect[1]))
                self.moneys.add(money)

    def jump_check(self):
        global up_counter
        global jump_state
        player = self.player.sprite
        for platform in self.platforms:
            if player.rect.bottom == platform.rect.top:
                jump_state = True
                up_counter = 0
        if up_counter != 2 and jump_state:
            player.jump()
            up_counter += 1
        if up_counter == 2:
            up_counter = 0
            jump_state = False

    def enemy_attack(self):
        for mob in self.mobs:
            if pygame.sprite.collide_rect(mob, self.collision.sprite):
                player_stats.get_damage(100)
                display.hp_subtraction(100)
                print(player_stats.hp)

    def check_enemy(self):
        for mob in self.mobs:
            if mob.x_pos + 60 <= mob.step_counter:
                mob.v = -3
                mob.image = pygame.transform.flip(mob.image, True, False)
            if mob.x_pos - 60 >= mob.step_counter:
                mob.v = 3
                mob.image = pygame.transform.flip(mob.image, True, False)
            mob.rect.x += mob.v
            mob.step_counter += mob.v

    def open_checkpoint(self):
        player = self.player.sprite
        for point in self.checkpoints:
            if pygame.sprite.collide_rect(point, player):
                self.screen.blit(point.e_key_image, (point.rect.x + 25, point.rect.y - 60))
                point.interaction()

    def run(self):
        self.platforms.update(self.camera)
        self.platforms.draw(self.screen)
        self.moneys.update(self.camera)
        self.moneys.draw(self.screen)
        # self.vertical_borders.draw(self.screen)
        # self.vertical_borders.update(self.camera)
        self.camera_level()
        self.player.update()
        self.collision.update(self.player.sprite)
        self.vertical()
        self.horizontal()
        self.get_money()
        self.check_enemy()
        self.enemy_attack()
        self.open_checkpoint()
        self.mobs.update(self.camera)
        self.mobs.draw(self.screen)
        self.shops.update(self.camera)
        self.shops.draw(self.screen)
        self.checkpoints.update(self.camera)
        self.checkpoints.draw(self.screen)
        self.player.draw(self.screen)
        #self.collision.draw(self.screen)
