import pygame
from sys import exit
import random

pygame.init()

# Window size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball vs Rectangles")

clock = pygame.time.Clock()

# --------------------------
# PLAYER BALL
# --------------------------
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_radius = 20
ball_speed = 5
ball_color = (0, 150, 255)

# --------------------------
# ENEMY RECTANGLES
# --------------------------
enemies = []
for i in range(5):   # 5 enemies
    rect_x = random.randint(-500, -50)   # spawn off-screen
    rect_y = random.randint(50, HEIGHT - 50)
    rect_width = 120
    rect_height = 25
    speed = random.randint(3, 7)
    enemies.append([rect_x, rect_y, rect_width, rect_height, speed])


# --------------------------
# GAME OVER FUNCTION
# --------------------------
def game_over():
    font = pygame.font.SysFont("Arial", 60)
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 30))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    exit()


# --------------------------
# MAIN GAME LOOP
# --------------------------
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    # Player movement: Arrows + WASD
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ball_x -= ball_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ball_x += ball_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        ball_y -= ball_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        ball_y += ball_speed

    # Stay inside window
    ball_x = max(ball_radius, min(WIDTH - ball_radius, ball_x))
    ball_y = max(ball_radius, min(HEIGHT - ball_radius, ball_y))

    # Move enemies
    for enemy in enemies:
        enemy[0] += enemy[4]   # move right

        if enemy[0] > WIDTH:   # respawn
            enemy[0] = random.randint(-400, -100)
            enemy[1] = random.randint(50, HEIGHT - 50)
            enemy[4] = random.randint(3, 7)

        # Collision detection (circle vs rectangle)
        rect = pygame.Rect(enemy[0], enemy[1], enemy[2], enemy[3])
        dist_x = abs(ball_x - rect.centerx)
        dist_y = abs(ball_y - rect.centery)

        if dist_x < rect.width // 2 + ball_radius and dist_y < rect.height // 2 + ball_radius:
            game_over()

    # Drawing
    screen.fill((20, 20, 20))

    # Draw ball
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), (enemy[0], enemy[1], enemy[2], enemy[3]))

    pygame.display.flip()
    clock.tick(60)
