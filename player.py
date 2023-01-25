import pygame

map1 = open("maps/map1.txt").readlines()
size_x = 50


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill("purple")
        self.rect = self.image.get_rect(topleft=pos)

        self.vector = pygame.math.Vector2(0, 0)
        self.v = 10
        # характеристики прыжка
        self.gravity = 0.3
        self.v_jump = -5
        self.hp = 0
        self.lose = False

    def get_key(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.vector.x = 1
        elif keys[pygame.K_a]:
            self.vector.x = -1
        else:
            self.vector.x = 0

        if keys[pygame.K_SPACE]:
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
        # if self.lose:
        # f = pygame.font.Font(None, 70)
        # text = f.render("you've lost", 1, "red")
        # screen.blit(text, (300, 250))
