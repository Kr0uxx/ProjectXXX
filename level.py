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
location = "village"


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
    боково-поверхностные правые(J), всякие(A), боковые правые(R), 
    боково-нижние левые(D), боково-нижние правые(N), нижние средние(H)'''

    def type(self, typ):
        global location
        # тут лучше потом переделать хранение через словарь))
        if typ == 'X':
            self.image = pygame.image.load(f'tile assets\\{location} tiles\\town01.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'R':
            self.image = pygame.image.load(f'tile assets\\{location} tiles\\town02.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'L':
            self.image = pygame.image.load(f'tile assets\\{location} tiles\\town07.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'Z':
            self.image = pygame.image.load(f'tile assets\\{location} tiles\\town03.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'I':
            self.image = pygame.image.load(f'tile assets\\{location} tiles\\town04.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'J':
            self.image = pygame.image.load(f'tile assets\\{location} tiles\\town05.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'A':
            self.image = pygame.image.load(f'tile assets\\{location} tiles\\town06.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'D':
            self.image = pygame.image.load(f'tile assets\\{location} tiles\\town08.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'H':
            self.image = pygame.image.load(f'tile assets\\{location} tiles\\town09.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'N':
            self.image = pygame.image.load(f'tile assets\\{location} tiles\\town10.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))


class Props(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.size = size
        self.image = pygame.image.load('graphics\\tiles\\town01.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(bottomleft=pos)

    def update(self, shift):
        self.rect.x += shift

    def type(self, typ):
        props = {"T": ["tile assets\\village props\\tree_2.png", (250, 250)],
                 "t": ["tile assets\\village props\\tree_1.png", (250, 250)],
                 "m": ["tile assets\\village props\\barrel.png", (70, 70)],
                 "x": ["tile assets\\village props\\bag.png", (50, 50)],
                 "e": ["tile assets\\village props\\box_1.png", (50, 50)],
                 "B": ["tile assets\\village props\\box_2.png", (70, 70)],
                 "b": ["tile assets\\village props\\box_3.png", (50, 50)],
                 "j": ["tile assets\\village props\\ear_1.png", (100, 50)],
                 "i": ["tile assets\\village props\\ear_2.png", (50, 50)],
                 "F": ["tile assets\\village props\\flowers.png", (120, 70)],
                 "f": ["tile assets\\village props\\fire.png", (90, 40)],
                 "w": ["tile assets\\village props\\wall.png", (170, 70)],
                 "W": ["tile assets\\village props\\well.png", (150, 100)],
                 "o": ["tile assets\\village props\\target.png", (50, 50)],
                 "O": ["tile assets\\village props\\scarecrow.png", (100, 100)],
                 "l": ["tile assets\\village props\\logs.png", (100, 50)],
                 "c": ["tile assets\\village props\\sign_2.png", (100, 100)],
                 "s": ["tile assets\\village props\\sign_1.png", (80, 80)],
                 "a": ["tile assets\\town props\\sign.png", (100, 100)],
                 "p": ["tile assets\\village props\\pumpkin.png", (100, 50)],
                 "G": ["tile assets\\village props\\grave_1.png", (50, 50)],
                 "g": ["tile assets\\village props\\grave_2.png", (50, 50)],
                 "Q": ["tile assets\\village props\\statue.png", (70, 170)],
                 "1": ["tile assets\\village props\\grass_1.png", (30, 30)],
                 "2": ["tile assets\\village props\\grass_2.png", (30, 30)],
                 "3": ["tile assets\\village props\\grass_3.png", (30, 30)],
                 "4": ["tile assets\\village props\\grass_4.png", (30, 30)],
                 "5": ["tile assets\\town props\\grass_1.png", (30, 30)],
                 "6": ["tile assets\\town props\\grass_2.png", (30, 30)],
                 "7": ["tile assets\\town props\\grass_3.png", (30, 30)],
                 "8": ["tile assets\\village props\\bush_1.png", (100, 50)],
                 "9": ["tile assets\\village props\\bush_2.png", (170, 70)],
                 "0": ["tile assets\\village props\\bush_3.png", (170, 70)],
                 "+": ["tile assets\\village props\\rock_1.png", (90, 40)],
                 "-": ["tile assets\\village props\\rock_2.png", (100, 50)],
                 "=": ["tile assets\\village props\\rock_3.png", (90, 40)],
                 "<": ["tile assets\\town props\\rock_1.png", (80, 30)],
                 ">": ["tile assets\\town props\\rock_2.png", (80, 30)],
                 "*": ["tile assets\\town props\\rock_3.png", (100, 50)],
                 "!": ["tile assets\\town props\\lamp.png", (30, 80)],
                 ":": ["tile assets\\village props\\straw_1.png", (120, 70)],
                 ";": ["tile assets\\village props\\straw_2.png", (100, 50)],
                 ".": ["tile assets\\village props\\jug_2.png", (30, 30)],
                 ",": ["tile assets\\village props\\jug_3.png", (30, 30)],
                 "@": ["tile assets\\village props\\fence_1.png", (120, 70)],
                 "#": ["tile assets\\village props\\fence_2.png", (120, 70)],
                 "%": ["tile assets\\village props\\fence_3.png", (100, 50)],
                 "&": ["tile assets\\town props\\fence_1.png", (150, 50)],
                 "$": ["tile assets\\town props\\fence_2.png", (150, 50)]
                 }
        self.image = pygame.image.load(props[typ][0])
        self.image = pygame.transform.scale(self.image, props[typ][1])


class Level:
    def __init__(self, map2, screen):
        self.screen = screen
        self.read(map2)
        self.camera = 0
        self.money = 0

    def read(self, map2):
        props = {"T": ["tile assets\\village props\\tree_2.png", (250, 250)],
                 "t": ["tile assets\\village props\\tree_1.png", (250, 250)],
                 "m": ["tile assets\\village props\\barrel.png", (70, 70)],
                 "x": ["tile assets\\village props\\bag.png", (50, 50)],
                 "e": ["tile assets\\village props\\box_1.png", (50, 50)],
                 "B": ["tile assets\\village props\\box_2.png", (70, 70)],
                 "b": ["tile assets\\village props\\box_3.png", (50, 50)],
                 "j": ["tile assets\\village props\\ear_1.png", (100, 50)],
                 "i": ["tile assets\\village props\\ear_2.png", (50, 50)],
                 "F": ["tile assets\\village props\\flowers.png", (120, 70)],
                 "f": ["tile assets\\village props\\fire.png", (90, 40)],
                 "w": ["tile assets\\village props\\wall.png", (170, 70)],
                 "W": ["tile assets\\village props\\well.png", (150, 100)],
                 "o": ["tile assets\\village props\\target.png", (50, 50)],
                 "O": ["tile assets\\village props\\scarecrow.png", (100, 100)],
                 "l": ["tile assets\\village props\\logs.png", (100, 50)],
                 "c": ["tile assets\\village props\\sign_2.png", (100, 100)],
                 "s": ["tile assets\\village props\\sign_1.png", (80, 80)],
                 "a": ["tile assets\\town props\\sign.png", (100, 100)],
                 "p": ["tile assets\\village props\\pumpkin.png", (100, 50)],
                 "G": ["tile assets\\village props\\grave_1.png", (50, 50)],
                 "g": ["tile assets\\village props\\grave_2.png", (50, 50)],
                 "Q": ["tile assets\\village props\\statue.png", (70, 170)],
                 "1": ["tile assets\\village props\\grass_1.png", (30, 30)],
                 "2": ["tile assets\\village props\\grass_2.png", (30, 30)],
                 "3": ["tile assets\\village props\\grass_3.png", (30, 30)],
                 "4": ["tile assets\\village props\\grass_4.png", (30, 30)],
                 "5": ["tile assets\\town props\\grass_1.png", (30, 30)],
                 "6": ["tile assets\\town props\\grass_2.png", (30, 30)],
                 "7": ["tile assets\\town props\\grass_3.png", (30, 30)],
                 "8": ["tile assets\\village props\\bush_1.png", (100, 50)],
                 "9": ["tile assets\\village props\\bush_2.png", (170, 70)],
                 "0": ["tile assets\\village props\\bush_3.png", (170, 70)],
                 "+": ["tile assets\\village props\\rock_1.png", (90, 40)],
                 "-": ["tile assets\\village props\\rock_2.png", (100, 50)],
                 "=": ["tile assets\\village props\\rock_3.png", (90, 40)],
                 "<": ["tile assets\\town props\\rock_1.png", (80, 30)],
                 ">": ["tile assets\\town props\\rock_2.png", (80, 30)],
                 "*": ["tile assets\\town props\\rock_3.png", (100, 50)],
                 "!": ["tile assets\\town props\\lamp.png", (30, 80)],
                 ":": ["tile assets\\village props\\straw_1.png", (120, 70)],
                 ";": ["tile assets\\village props\\straw_2.png", (100, 50)],
                 ".": ["tile assets\\village props\\jug_2.png", (30, 30)],
                 ",": ["tile assets\\village props\\jug_3.png", (30, 30)],
                 "@": ["tile assets\\village props\\fence_1.png", (120, 70)],
                 "#": ["tile assets\\village props\\fence_2.png", (120, 70)],
                 "%": ["tile assets\\village props\\fence_3.png", (100, 50)],
                 "&": ["tile assets\\town props\\fence_1.png", (150, 50)],
                 "$": ["tile assets\\town props\\fence_2.png", (150, 50)]
                 }
        self.platforms = pygame.sprite.Group()
        self.props = pygame.sprite.Group()
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
                if c == "X" or c == "L" or c == "R" or c == "Z" or c == "I" or c == "J" or c == "A"\
                        or c == "D" or c == "H" or c == "N":
                    platform = Platform((size_x * ind_c, size_x * ind_r), size_x)
                    platform.type(c)
                    self.platforms.add(platform)
                elif c == "T" or c == "t" or c == "B" or c == "b" or c == "m" or c == "x" or c == "e" or c == "j"\
                        or c == "i" or c == "F" or c == "f" or c == "W" or c == "w" or c == "O" or c == "o" \
                        or c == "l" or c == "c" or c == "s" or c == "a" or c == "p" or c == "G" or c == "g" \
                        or c == "Q" or c == "1" or c == "2" or c == "3" or c == "4" or c == "5" or c == "6" or c == "7"\
                        or c == "8" or c == "9" or c == "0" or c == "+" or c == "-" or c == "=" or c == ">" or c == "<"\
                        or c == "*" or c == "!" or c == ":" or c == ";" or c == "." or c == ","\
                        or c == "@" or c == "#" or c == "%" or c == "&" or c == "$":
                    prop = Props((size_x * ind_c, size_x * (ind_r + 1 + (props[c][1][0] - props[c][1][1]) // 50)), props[c][1][0])
                    prop.type(c)
                    self.props.add(prop)
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
        self.props.update(self.camera)
        self.props.draw(self.screen)
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
        #self.collision.draw(self.screen)


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
