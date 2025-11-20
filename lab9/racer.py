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

    #  төмен қарай жылжиды
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)

        # егер экраннан шығып кетсе — қайта жоғары шығады
        if self.rect.top > HEIGHT:
            SCORE += 1   # әр өткен жауға балл қосылады
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images2/coin.png")
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()

        self.weight = random.choice([1, 2, 3])

        # монета жолдың кез келген жерінде пайда болады
        self.rect.center = (random.randint(40, WIDTH - 40), -40)

    # монетаның төмен түсу жылжуы
    def move(self):
        self.rect.move_ip(0, SPEED)

        # экраннан шықса — жаңадан spawn
        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        # жаңа монета — жаңа weight
        self.weight = random.choice([1, 2, 3])
        self.rect.center = (random.randint(40, WIDTH - 40), -40)

    # монета жиналғанда
    def collect(self):
        global COINS, SPEED
        COINS += self.weight     # салмағына қарай санына қосылады

        # әр 10 монет сайын жылдамдық артады
        if COINS % 10 == 0:
            SPEED += 1

        self.reset()

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


# заттарды құру
player = Player()
enemy = Enemy()
coin = Coin()

enemies = pygame.sprite.Group()
enemies.add(enemy)

coins = pygame.sprite.Group()
coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, coin)


# Ойынның аяқталуы 
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

    # враг
    if pygame.sprite.spritecollideany(player, enemies):
        game_over()

    # монетаны collect
    coin_hit = pygame.sprite.spritecollideany(player, coins)
    if coin_hit:
        coin_hit.collect()

    screen.blit(background, (0, 0))

    # барлық объектілерді жылжыту және салу
    for obj in all_sprites:
        obj.move()
        screen.blit(obj.image, obj.rect)

    # экранға текст шығару
    score_text = font.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font.render(f"Coins: {COINS}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(coin_text, (310, 10))

    pygame.display.update()
    clock.tick(FPS)
