import pygame, sys
from pygame.locals import *
import random, time

pygame.init()


WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


background = pygame.image.load("images2/AnimatedStreet.png")
font = pygame.font.SysFont("Verdana", 20)

FPS = 60
clock = pygame.time.Clock()
SPEED = 3
SCORE = 0
COINS = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images2/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)

    
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images2/coin.png")
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), -40)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(40, WIDTH - 40), -40)

    def collect(self):
        global COINS, SPEED
        COINS += 1
        if COINS % 10 == 0:
            SPEED += 1
        self.rect.center = (random.randint(40, WIDTH - 40), -40)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images2/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(5, 0)
        

player = Player()
enemy = Enemy()
coin = Coin()

enemies = pygame.sprite.Group()
enemies.add(enemy)

coins = pygame.sprite.Group()
coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, coin)

def game_over():
    screen.fill((255, 0, 0))
    text = font.render("GAME OVER", True, BLACK)
    screen.blit(text, (130, 250))
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if pygame.sprite.spritecollideany(player, enemies):
        game_over()

    coin_hit = pygame.sprite.spritecollideany(player, coins)
    if coin_hit:
        coin_hit.collect()

    screen.blit(background, (0, 0))

    for obj in all_sprites:
        obj.move()
        screen.blit(obj.image, obj.rect)

    score_text = font.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font.render(f"Coins: {COINS}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(coin_text, (310, 10))

    pygame.display.update()
    clock.tick(FPS)