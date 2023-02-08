import pygame
from player import Player
from player import Collision
from mob import Mob
from shop import Shop
# from border import Border
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


def animation(clas, frame, col, size1, size2):
    pass
    #images = []
    #for i in range(col):
        #images.append(
            #pygame.transform.scale(pygame.image.load(f'graphics\\Characters\\Hero\\idle\\{frame}-0{i + 1}.png'), (size1, size2)))
    #n = 0
    #clas.image = images[n]
    #n += 1
    #if n >= len(images):
        #n = 0
    #clas.image = images[n]


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


class Level:
    def __init__(self, map2, screen):
        self.screen = screen
        self.read(map2)
        self.camera = 0
        self.money = 0

    def read(self, map2):
        self.platforms = pygame.sprite.Group()
        self.vertical_borders = pygame.sprite.Group()
        self.moneys = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.collision = pygame.sprite.GroupSingle()
        self.mobs = pygame.sprite.Group()
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
        global player_v
        player = self.player.sprite
        playerx = player.rect.centerx
        playery = player.rect.centery
        vectorx = player.vector.x
        vectory = player.vector.y
        if (self.vert1.rect.x < width / 1000 or self.vert1.rect.x > width * 999 / 1000) and \
                (self.vert2.rect.x < width / 1000 or self.vert2.rect.x > width * 999 / 1000):
            if playerx <= width / 2 and vectorx < 0:
                self.camera = player_v
                player.v = 0
            elif playerx >= width / 2 and vectorx > 0:
                self.camera = -player_v
                player.v = 0
            else:
                self.camera = 0
                player.v = player_v
        else:
            if self.vert1.rect.x >= width / 1000 and playerx < width / 2:
                self.camera = 0
                player.v = player_v
            elif self.vert2.rect.x <= width * 999 / 1000 and playerx > width / 2:
                self.camera = 0
                player.v = -player_v
            if self.vert1.rect.x >= width / 1000 and playerx > width / 2:
                self.camera = -player_v
                player.v = 0
            elif self.vert2.rect.x <= width * 999 / 1000 and playerx < width / 2:
                self.camera = player_v
                player.v = 0
            else:
                self.camera = 0
                if self.vert2.rect.x <= width * 999 / 1000:
                    player.v = player_v
                elif self.vert1.rect.x >= width / 1000:
                    player.v = player_v

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

    def lr_border(self):
        player = self.player.sprite
        if self.vert1.rect.colliderect(player.rect):
            player.rect.left = self.vert1.rect.right
        if self.vert2.rect.colliderect(player.rect):
            player.rect.right = self.vert2.rect.left

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
        self.vertical_borders.draw(self.screen)
        self.vertical_borders.update(self.camera)
        self.camera_level()
        self.player.update()
        self.collision.update(self.player.sprite)
        self.vertical()
        self.horizontal()
        self.get_money()
        self.lr_border()
        self.open_checkpoint()
        self.mobs.update(self.camera)
        self.mobs.draw(self.screen)
        self.shops.update(self.camera)
        self.shops.draw(self.screen)
        self.checkpoints.update(self.camera)
        self.checkpoints.draw(self.screen)
        self.player.draw(self.screen)
        self.collision.draw(self.screen)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:  # вертикальная стенка
            self.image = pygame.Surface([0.5, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)

    def update(self, shift):
        self.rect.x += shift


size = width, height
screen = pygame.display.set_mode(size)
level = Level(map1, screen)
