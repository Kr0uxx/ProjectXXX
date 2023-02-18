import pygame
from player import Player, Collision, PlayerStats, Effect
from mob import Mob
from boss import Boss
from shop import Shop
from checkpoint import CheckPoint
from checkpoints_display import PointsDisplay
from random import randint
from display import Display
from wizard import Wizard

map1 = open("maps/map1.txt").readlines()
size_x = 50
width = 1920
status = 'start'
hp = 100
damage = 5
up_counter = 0
jump_state = False
location = 'village'
props = {"T": ["graphics\\props\\village\\tree_2.png", (250, 250)],
         "t": ["graphics\\props\\village\\tree_1.png", (250, 250)],
         "m": ["graphics\\props\\village\\barrel.png", (70, 70)],
         "x": ["graphics\\props\\village\\bag.png", (50, 50)],
         "e": ["graphics\\props\\village\\box_1.png", (50, 50)],
         "B": ["graphics\\props\\village\\box_2.png", (70, 70)],
         "b": ["graphics\\props\\village\\box_3.png", (50, 50)],
         "j": ["graphics\\props\\village\\ear_1.png", (100, 50)],
         "i": ["graphics\\props\\village\\ear_2.png", (50, 50)],
         "F": ["graphics\\props\\village\\flowers.png", (120, 70)],
         "f": ["graphics\\props\\village\\fire.png", (90, 40)],
         "w": ["graphics\\props\\village\\wall.png", (170, 70)],
         "W": ["graphics\\props\\village\\well.png", (150, 100)],
         "o": ["graphics\\props\\village\\target.png", (50, 50)],
         "O": ["graphics\\props\\village\\scarecrow.png", (100, 100)],
         "l": ["graphics\\props\\village\\logs.png", (100, 50)],
         "c": ["graphics\\props\\village\\sign_2.png", (100, 100)],
         "s": ["graphics\\props\\village\\sign_1.png", (80, 80)],
         "a": ["graphics\\props\\village\\sign.png", (100, 100)],
         "p": ["graphics\\props\\village\\pumpkin.png", (100, 50)],
         "G": ["graphics\\props\\village\\grave_1.png", (50, 50)],
         "g": ["graphics\\props\\village\\grave_2.png", (50, 50)],
         "Q": ["graphics\\props\\village\\statue.png", (70, 170)],
         "1": ["graphics\\props\\village\\grass_1.png", (30, 30)],
         "2": ["graphics\\props\\village\\grass_2.png", (30, 30)],
         "3": ["graphics\\props\\village\\grass_3.png", (30, 30)],
         "4": ["graphics\\props\\village\\grass_4.png", (30, 30)],
         "5": ["graphics\\props\\village\\grass_1.png", (30, 30)],
         "6": ["graphics\\props\\village\\grass_2.png", (30, 30)],
         "7": ["graphics\\props\\village\\grass_3.png", (30, 30)],
         "8": ["graphics\\props\\village\\bush_1.png", (100, 50)],
         "9": ["graphics\\props\\village\\bush_2.png", (170, 70)],
         "0": ["graphics\\props\\village\\bush_3.png", (170, 70)],
         "+": ["graphics\\props\\village\\rock_1.png", (90, 40)],
         "-": ["graphics\\props\\village\\rock_2.png", (100, 50)],
         "=": ["graphics\\props\\village\\rock_3.png", (90, 40)],
         "<": ["graphics\\props\\village\\rock_1.png", (80, 30)],
         ">": ["graphics\\props\\village\\rock_2.png", (80, 30)],
         "*": ["graphics\\props\\village\\rock_3.png", (100, 50)],
         "!": ["graphics\\props\\village\\lamp.png", (30, 80)],
         ":": ["graphics\\props\\village\\straw_1.png", (120, 70)],
         ";": ["graphics\\props\\village\\straw_2.png", (100, 50)],
         ".": ["graphics\\props\\village\\jug_2.png", (30, 30)],
         ",": ["graphics\\props\\village\\jug_3.png", (30, 30)],
         "@": ["graphics\\props\\village\\fence_1.png", (120, 70)],
         "#": ["graphics\\props\\village\\fence_2.png", (120, 70)],
         "%": ["graphics\\props\\village\\fence_3.png", (100, 50)],
         "&": ["graphics\\props\\village\\fence_1.png", (150, 50)],
         "$": ["graphics\\props\\village\\fence_2.png", (150, 50)]
         }


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
        self.image = pygame.image.load('graphics/tiles/town/town01.png')
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
        if typ == 'X':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town01.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'R':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town02.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'L':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town07.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'Z':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town03.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'I':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town04.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'J':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town05.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'A':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town06.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'D':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town08.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'H':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town09.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'N':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town10.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'p':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town11.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'u':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town12.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == '_':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town13.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif typ == 'Y':
            self.image = pygame.image.load(f'graphics\\tiles\\{location}\\town14.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))


class Props(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.size = size
        self.image = pygame.image.load('graphics\\tiles\\town\\town01.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(bottomleft=pos)

    def update(self, shift):
        self.rect.x += shift

    def type(self, typ):
        self.image = pygame.image.load(props[typ][0])
        self.image = pygame.transform.scale(self.image, props[typ][1])


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
        self.effect = pygame.sprite.GroupSingle()
        self.mobs = pygame.sprite.Group()
        self.boss = pygame.sprite.GroupSingle()
        self.shops = pygame.sprite.Group()
        self.wizard = pygame.sprite.GroupSingle()
        self.checkpoints = pygame.sprite.Group()
        self.transitions = pygame.sprite.Group()
        self.props = pygame.sprite.Group()
        for ind_r, r in enumerate(map2):
            for ind_c, c in enumerate(r):
                if c == "X" or c == "L" or c == "R" or c == "Z" or c == "I" or c == "J" or c == "A" \
                        or c == "D" or c == "H" or c == "N" or c == "p" or c == 'u' or c == '_' or c == 'Y':
                    platform = Platform((size_x * ind_c, size_x * ind_r), size_x)
                    platform.type(c)
                    self.platforms.add(platform)
                elif c == "T" or c == "t" or c == "B" or c == "b" or c == "m" or c == "x" or c == "e" or c == "j" \
                        or c == "i" or c == "F" or c == "f" or c == "W" or c == "w" or c == "O" or c == "o" \
                        or c == "l" or c == "c" or c == "s" or c == "a" or c == "p" or c == "G" or c == "g" \
                        or c == "Q" or c == "1" or c == "2" or c == "3" or c == "4" or c == "5" or c == "6" or c == "7" \
                        or c == "8" or c == "9" or c == "0" or c == "+" or c == "-" or c == "=" or c == ">" or c == "<" \
                        or c == "*" or c == "!" or c == ":" or c == ";" or c == "." or c == "," \
                        or c == "@" or c == "#" or c == "%" or c == "&" or c == "$":
                    prop = Props(
                        (size_x * ind_c, size_x * (ind_r + 1 + (props[c][1][0] - props[c][1][1]) // 50)),
                        props[c][1][0])
                    prop.type(c)
                    self.props.add(prop)
                elif c == "P":
                    # pos = size_x * ind_c, size_x * ind_r
                    player = Player((size_x * ind_c, size_x * ind_r))
                    pos = (size_x * ind_c, size_x * ind_r)
                    self.player.add(player)
                    collision = Collision((size_x * ind_c, size_x * ind_r), self.player.sprite)
                    self.collision.add(collision)
                    effect = Effect((size_x * ind_c, size_x * ind_r))
                    self.effect.add(effect)
                    self.player.effect = self.effect
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
                elif c == 'U':
                    wizard = Wizard((size_x * ind_c, size_x * ind_r), self.screen)
                    self.wizard.add(wizard)
                elif c == 'C':
                    checkpoint = CheckPoint((size_x * ind_c, size_x * ind_r), self.screen)
                    print((size_x * ind_c, size_x * ind_r))
                    self.checkpoints.add(checkpoint)
                '''elif c == 'h':
                    transition = Transition((size_x * ind_c, size_x * ind_r), self.screen)
                    print((size_x * ind_c, size_x * ind_r))
                    self.transitions.add(transition)'''
        return pos

    def camera_level(self):
        player = self.player.sprite
        playerx = player.rect.centerx
        playery = player.rect.centery
        vectorx = player.vector.x
        vectory = player.vector.y
        if playerx <= width / 2 and vectorx < 0:
            self.camera = 10
            player.v = 0
        elif playerx > width / 2 and vectorx > 0:
            self.camera = -10
            player.v = 0
        else:
            self.camera = 0
            player.v = 10

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
        f_shadow = pygame.font.Font('dialogs\\fonts\\header_font.ttf', 58)
        f = pygame.font.Font('dialogs\\fonts\\header_font.ttf', 49)
        text_shadow = f_shadow.render(str(self.money), True, (0, 0, 0))
        text = f.render(str(self.money), True, (233, 211, 3))
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

    '''def transition_interaction(self):
        player = self.player.sprite
        for transition in self.transitions:
            if pygame.sprite.collide_rect(transition, player):
                x = transition.pos[0]
                if transition.transitions[map1, transition.pos] % 2 == 1:
                    x -= transition.transitions[transition.pos[0]]
                self.camera_centred(-x)
                return transition.interaction(player)'''

    def shop_collision(self):
        player = self.player.sprite
        for shop in self.shops:
            if pygame.sprite.collide_rect(shop, player):
                self.screen.blit(self.e_key_image, (shop.rect.x + 100, shop.rect.y - 30))
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    return shop.interaction(1)

    def wizard_collision(self):
        player = self.player.sprite
        wizard = self.wizard.sprite
        if pygame.sprite.collide_rect(wizard, player):
            self.screen.blit(self.e_key_image, (wizard.rect.x + 100, wizard.rect.y - 70))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                return wizard.interaction(6)

    def camera_centred(self, x):
        self.platforms.update(x)
        self.props.update(x)
        self.moneys.update(x)
        self.mobs.update(x)
        self.shops.update(x)
        self.wizard.update(x)
        self.checkpoints.update(x)

    # the worst code i`ve ever seen
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

    # говнокод, переписать
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
                if mob.attack_delay == 30:
                    self.player_stats.get_damage(mob.damage)
                    self.display.hp_subtraction(mob.damage)
                    print(self.player_stats.hp)
                    print(mob.attack_delay)
                    mob.attack_delay = 0
                else:
                    mob.attack_delay += 1

    def check_enemy(self):
        for mob in self.mobs:
            if not pygame.sprite.collide_rect(mob, self.collision.sprite):
                if mob.x_pos + 60 <= mob.step_counter:
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
        self.props.update(self.camera)
        self.props.draw(self.screen)

        # 2 слой - пропсы
        self.moneys.update(self.camera)
        self.moneys.draw(self.screen)

        self.checkpoints.update(self.camera)
        self.checkpoints.draw(self.screen)
        # 3 слой мобы, нпс
        self.mobs.update(self.camera)
        self.mobs.draw(self.screen)
        self.boss.draw(self.screen)
        for shop in self.shops:
            shop.animate_npc(shop.images, 6, False, (250, 250))
        self.shops.update(self.camera)
        self.shops.draw(self.screen)
        wizard = self.wizard.sprite
        wizard.animate_npc(wizard.images, 14, False, (250, 300))
        self.wizard.update(self.camera)
        self.wizard.draw(self.screen)

        # 4 слой - игрок
        self.player.update()
        self.player.draw(self.screen)
        self.collision.update(self.player.sprite)
        self.vertical()
        self.horizontal()
        self.effect.update(self.player.sprite)
        if self.player.sprite.status == 'attack':
            if self.player.sprite.orientation == 'left':
                self.effect.sprite.animate_effect('graphics\\effects\\attack_effect\\SFX301', 5, False)
            else:
                self.effect.sprite.animate_effect('graphics\\effects\\attack_effect\\SFX301', 5, True)
            self.effect.draw(self.screen)
            if self.effect.sprite.cur_frame == 4:
                self.player.sprite.status = 'stand'
        # 5 слой - функции
        self.shop_collision()
        self.wizard_collision()
        self.get_money()
        self.open_checkpoint()
        self.enemy_attack()
        self.check_enemy()
        player = self.player.sprite
        # 6 слой дисплей
        self.display.run()
