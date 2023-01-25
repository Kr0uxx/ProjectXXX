import pygame
import sys

#карта для уровня
map1 = [
'                                                   ',
'                                         M         ',
'         M             M              XXXXXXXXXX   ',
' XX    XXX            XX                           ',
'MXX P                         XXXXXX               ',
'XXXXX        XXX         XX           XXXXX     M  ',
' XXXX       XX                    M XXX       XXXXX',
' XX    X  XXXX    XX  XX          XXX              ',
'       X  XXXX M  XX  XXX                XXXX      ',
'  M XXXX  XXXXXX  XX  XXXX  M XX         XX    M   ',
'XXXXXXXX  XXXX    XX  XXXX  XXXXX        XX   XXXXX']

pygame.init()

size_x = 50
width = 800
height = len(map1) * size_x

size = width, height
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = pos)
        self.image.fill("black")

    def update(self, shift):
        #сдвиг платформ при движении камеры
        self.rect.x += shift


class Money(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect(topleft = pos)
        self.image.fill("orange")

    def update(self, shift):
        #сдвиг монеток при движении камеры
        self.rect.x += shift



class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill("purple")
        self.rect = self.image.get_rect(topleft = pos)

        self.vector = pygame.math.Vector2(0,0)
        self.v = 5
        #характеристики прыжка
        self.gravity = 0.3
        self.v_jump = -5
        self.lose = False

    def get_key(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vector.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vector.x = -1
        else:
            self.vector.x = 0

        if keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[pygame.K_w]:
            self.jump()

    def with_gravity(self):
        self.vector.y += self.gravity
        self.rect.y += self.vector.y

    def jump(self):
        self.vector.y = self.v_jump

    def update(self):
        self.get_key()
        if not self.lose:
            if self.rect.y > len(map1) * size_x:
                self.lose = True
                print("you've lost")
        if self.lose:
            f = pygame.font.Font(None, 70)
            text = f.render("you've lost", 1, "red")
            screen.blit(text, (300, 250))


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
        if playerx <= width / 2 and vectorx < 0:
            self.camera = 5
            player.v = 0
        elif playerx >= width / 2 and vectorx > 0:
            self.camera = -5
            player.v = 0
        #elif playery > height / 2 and vectory > 0:
            #self.camera = 5
            #player.v = 0
        #elif playery < height / 2 and vectory < 0:
            #self.camera = -5
            #player.v = 0
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
        global count_money
        player = self.player.sprite
        for money in self.moneys:
            if pygame.sprite.collide_rect(money, player):
                money.kill()
                count_money += 1
                print(count_money)
        f = pygame.font.Font(None, 40)
        text = f.render(f"money: {str(count_money)}", 1, "black")
        screen.blit(text, (20, 30))



    def run(self):
        self.platforms.update(self.camera)
        self.platforms.draw(self.surface)
        self.moneys.update(self.camera)
        self.moneys.draw(self.surface)
        self.get_money()
        self.camera_level()
        self.player.update()
        self.vertical()
        self.horizontal()
        self.player.draw(self.surface)


level = Level(map1, screen)
count_money = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")
    level.run()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()



