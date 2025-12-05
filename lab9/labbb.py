import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

background = pygame.image.load("images2/AnimatedStreet.png")
font = pygame.font.SysFont("Verdana", 20)

FPS = 60
clock = pygame.time.Clock()
SPEED = 3       
SCORE = 0      
COINS = 0       





class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images2/coin.png")
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()

        self.weight = random.choice([1])

        # монета жолдың кез келген жерінде пайда болады
        self.rect.center = (150, 200)

    # монетаның төмен түсу жылжуы
    def move(self):
        self.rect.move_ip(0, SPEED)

        # экраннан шықса — жаңадан spawn
        
        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        # жаңа монета — жаңа weight
        self.weight = random.choice([1])
        self.rect.center = (150, 200)

    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images2/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (100, 150)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(5, 0)
        


# заттарды құру
player = Player()

coin = Coin()



coins = pygame.sprite.Group()
coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player,  coin)


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

   
    

    # барлық объектілерді жылжыту және салу
    for obj in all_sprites:
        obj.move()
        screen.blit(obj.image, obj.rect)

    

    pygame.display.update()
    clock.tick(FPS)
