import pygame
from player import Player, Collision, PlayerStats
from mob import Mob
from boss import Boss
from shop import Shop
from checkpoint import CheckPoint
from checkpoints_display import PointsDisplay
from random import randint
from display import Display

map1 = open("maps/map1.txt").readlines()
size_x = 50
width = 1920
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


class Money(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect(topleft=pos)
        self.images = []
        for i in range(7):
            self.images.append(
                pygame.transform.scale(pygame.image.load(f'graphics\\props\\coin\\coin-0{i + 1}.png'),
                                       (30, 30)))
        self.n = 0
        self.image = self.images[self.n]

    def update(self, shift):
        self.n += 1
        if self.n >= len(self.images):
            self.n = 0
        self.image = self.images[self.n]
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
    def __init__(self, map2, screen, player_status):
        self.screen = screen
        self.read(map2)
        self.camera = 0
        self.money = 0
        self.status = player_status
        self.points_display = PointsDisplay(screen)
        self.e_key_image = pygame.image.load('graphics\\display\\keys\\e_key.png')
        self.e_key_image = pygame.transform.scale(self.e_key_image, (50, 50))
        self.player_stats = PlayerStats(status, 1000, 1000, damage)
        self.display = Display(screen, width, self.player_stats.hp, self.player_stats.mana)
        self.attack_enabled = False

    def read(self, map2, pos=(150, 450)):
        self.platforms = pygame.sprite.Group()
        self.moneys = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.collision = pygame.sprite.GroupSingle()
        self.mobs = pygame.sprite.Group()
        self.boss = pygame.sprite.GroupSingle()
        self.shops = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        self.vert1 = Border(0, 0, 0, height)
        self.vert2 = Border(map_w, 0, map_w, height)
        self.vertical_borders.add(self.vert1)
        self.vertical_borders.add(self.vert2)
        for ind_r, r in enumerate(map2):
            for ind_c, c in enumerate(r):
                if c == "X" or c == "L" or c == "R" or c == "Z" or c == "I" or c == "J" or c == "A":
                    platform = Platform((size_x * ind_c, size_x * ind_r), size_x)
                    platform.type(c)
                    self.platforms.add(platform)
                elif c == "P":
                    # pos = size_x * ind_c, size_x * ind_r
                    player = Player(pos)
                    self.player.add(player)
                    collision = Collision((size_x * ind_c, size_x * ind_r), self.player.sprite)
                    self.collision.add(collision)
                elif c == "M":
                    money = Money((size_x * ind_c, size_x * ind_r))
                    self.moneys.add(money)
                elif c == 'E':
                    enemy = Mob((size_x * ind_c, size_x * ind_r))
                    self.mobs.add(enemy)
                elif c == 'B':
                    boss = Boss((size_x * ind_c, size_x * ind_r))
                    self.boss.add(boss)
                elif c == 'S':
                    shop = Shop((size_x * ind_c, size_x * ind_r), self.screen)
                    self.shops.add(shop)
                elif c == 'C':
                    checkpoint = CheckPoint((size_x * ind_c, size_x * ind_r), self.screen)
                    print((size_x * ind_c, size_x * ind_r))
                    self.checkpoints.add(checkpoint)

        return pos

    def camera_level(self):
        player = self.player.sprite
        playerx = player.rect.centerx
        playery = player.rect.centery
        vectorx = player.vector.x
        vectory = player.vector.y
        if self.vert1.rect.x >= width / 1000 and playerx < width / 2:
            self.camera = 10
            player.v = 0
        elif self.vert2.rect.x <= width * 999 / 1000 and playerx > width / 2:
            self.camera = -10
            player.v = 0
        if self.vert1.rect.x >= width / 1000 and playerx > width / 2:
            self.camera = -10
            player.v = 0
        elif self.vert2.rect.x <= width * 999 / 1000 and playerx < width / 2:
            self.camera = 10
            player.v = 0
        else:
            self.camera = 0
            if self.vert2.rect.x <= width * 999 / 1000:
                player.v = 10
            elif self.vert1.rect.x >= width / 1000:
                player.v = 10

    def camera_centred(self, x):
        self.platforms.update(x)
        self.moneys.update(x)
        self.mobs.update(x)
        self.shops.update(x)
        self.checkpoints.update(x)

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

    def lr_border(self):
        player = self.player.sprite
        if self.vert1.rect.colliderect(player.rect):
            player.rect.left = self.vert1.rect.right
        if self.vert2.rect.colliderect(player.rect):
            player.rect.right = self.vert2.rect.left

    def get_money(self):
        player = self.player.sprite
        for money in self.moneys:
            if pygame.sprite.collide_rect(money, player):
                pygame.mixer.Sound('music\\sounds\\coin.wav').play()
                money.kill()
                self.money += 1
        f_shadow = pygame.font.Font('dialogs\\fonts\\header_font.ttf', 58)
        ff = pygame.font.Font('dialogs\\fonts\\header_font.ttf', 49)
        text_shadow = f_shadow.render(str(self.money), True, (0, 0, 0))
        text = ff.render(str(self.money), True, (233, 211, 3))
        image_display_coin = pygame.image.load('graphics\\props\\coin\\coin-01.png')
        image_display_coin = pygame.transform.scale(image_display_coin, (40, 40))
        self.screen.blit(image_display_coin, (30, 170))
        self.screen.blit(text_shadow, (72, 162))
        self.screen.blit(text, (74, 166))

    def open_checkpoint(self):
        player = self.player.sprite
        for point in self.checkpoints:
            if pygame.sprite.collide_rect(point, player):
                self.screen.blit(self.e_key_image, (point.rect.x + 25, point.rect.y - 60))
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    return point.interaction()

    def shop_collision(self):
        player = self.player.sprite
        for shop in self.shops:
            if pygame.sprite.collide_rect(shop, player):
                self.screen.blit(self.e_key_image, (shop.rect.x + 100, shop.rect.y - 30))
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    return shop.interaction()

    # уродская функция для ограничения колва прыжков, которая должна была лежать в классе плейер
    def jump_check(self):
        global up_counter
        global jump_state
        player = self.player.sprite
        for platform in self.platforms:
            if player.rect.bottom == platform.rect.top:
                jump_state = True
                up_counter = 0
        if up_counter != 1 and jump_state:
            player.jump()
            up_counter += 1
        if up_counter == 2:
            up_counter = 0
            jump_state = False

    # 3 уродских функции для моба, которые должны были лежать в самом мобе
    def enemy_hurt(self):
        player = self.player.sprite
        for mob in self.mobs:
            if pygame.sprite.collide_rect(mob, self.collision.sprite):
                player.attack(mob)
            if mob.health == 0:
                mob.kill()
                for i in range(randint(1, 3)):
                    money = Money((mob.rect[0] + randint(0, 50), mob.rect[1]))
                    self.moneys.add(money)

    def enemy_attack(self):
        for mob in self.mobs:
            if pygame.sprite.collide_rect(mob, self.collision.sprite):
                mob.v = 0
                mob.lever_attack = True
                if mob.attack_delay == 30:
                    self.player_stats.get_damage(mob.damage)
                    self.display.hp_subtraction(mob.damage)
                    print(self.player_stats.hp)
                    print(mob.attack_delay)
                    mob.attack_delay = 0
                else:
                    mob.attack_delay += 1
            else:
                if mob.lever_attack:
                    mob.v = 3
                    mob.lever_attack = False
                mob.attack_delay = 0

    def check_enemy(self):
        for mob in self.mobs:
            if mob.x_pos + 60 < mob.step_counter:
                mob.v = -3
                mob.image = pygame.transform.flip(mob.image, True, False)
            if mob.x_pos - 60 >= mob.step_counter:
                mob.v = 3
                mob.image = pygame.transform.flip(mob.image, True, False)
            mob.rect.x += mob.v
            mob.step_counter += mob.v

    def run(self):
        # 1 слой - камера, тайлы
        self.camera_level()
        self.platforms.update(self.camera)
        self.platforms.draw(self.screen)

        # 2 слой - пропсы
        self.moneys.update(self.camera)
        self.moneys.draw(self.screen)

        self.checkpoints.update(self.camera)
        self.checkpoints.draw(self.screen)
        # 3 слой мобы, нпс
        self.mobs.update(self.camera)
        self.mobs.draw(self.screen)
        self.boss.draw(self.screen)

        self.shops.update(self.camera)
        self.shops.draw(self.screen)

        # 4 слой - игрок
        self.player.update()
        self.player.draw(self.screen)
        self.collision.update(self.player.sprite)
        self.vertical()
        self.horizontal()
        self.lr_border()
        # 5 слой - функции
        self.shop_collision()
        self.get_money()
        self.open_checkpoint()
        self.enemy_attack()
        self.check_enemy()

        # 6 слой дисплей
        self.display.run()


size = width, height
screen = pygame.display.set_mode(size)
level = Level(map1, screen, 'game')


# очередной класс в этом файле
class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:  # вертикальная стенка
            self.add(level.vertical_borders)
            self.image = pygame.Surface([0.5, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)

    def update(self, shift):
        self.rect.x += shift
