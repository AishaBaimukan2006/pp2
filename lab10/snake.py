import pygame
import time
import random
import sys
import psycopg2
from config import load_config

pygame.init()
config = load_config()

def create_user(username):
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT id FROM "user" WHERE username=%s;', (username,))
                row = cur.fetchone()
                if row:
                    user_id = row[0]
                    print(f"Welcome back, {username}!")
                    return user_id

                cur.execute('INSERT INTO "user"(username) VALUES(%s) RETURNING id;', (username,))
                user_id = cur.fetchone()[0]
                conn.commit()
                print(f"New user created: {username}")
                return user_id
    except Exception as e:
        print("DB ERROR:", e)
        return None

def save_score(user_id, score):
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, score FROM user_score
                    WHERE user_id=%s ORDER BY score DESC LIMIT 1;
                """, (user_id,))
                row = cur.fetchone()
                if row and score <= row[1]:
                    print(f"Score {score} not saved (current high = {row[1]})")
                    return
                if row:
                    cur.execute('DELETE FROM user_score WHERE id=%s;', (row[0],))
                cur.execute('INSERT INTO user_score(user_id, score) VALUES (%s, %s);', (user_id, score))
                conn.commit()
                print(f"Score saved: {score}")
    except Exception as e:
        print("Save ERROR:", e)

window_x, window_y = 1000, 500
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
gray = pygame.Color(100, 100, 100)
pink = pygame.Color(255, 209, 220)

game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('Snake Game with DB')
fps = pygame.time.Clock()


snake_speed = 10
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
fruit_position = [random.randrange(1, window_x//10) * 10, random.randrange(1, window_y//10) * 10]
fruit_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0
level = 1
foods_eaten = 0
obstacles = []

def spawn_fruit():
    while True:
        new_fruit = [random.randrange(1, window_x//10) * 10,
                     random.randrange(1, window_y//10) * 10]
        if new_fruit not in snake_body and new_fruit not in obstacles:
            return new_fruit

def generate_obstacles(level):
    new_obstacles = []
    for _ in range(level * 3):
        x = random.randrange(0, window_x // 10) * 10
        y = random.randrange(0, window_y // 10) * 10
        new_obstacles.append([x, y])
    return new_obstacles

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def show_score():
    font = pygame.font.SysFont('times new roman', 30)
    score_surface = font.render(f'Score: {score} Level: {level}', True, white)
    game_window.blit(score_surface, (10, 10))

def game_over():
    save_score(user_id, score)
    draw_text(f'Game Over! Score: {score}', pygame.font.SysFont('times new roman', 50), red, game_window, window_x//2, window_y//2)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

username = input("Enter username: ")
user_id = create_user(username)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    direction = change_to
    if direction == 'UP': snake_position[1] -= 10
    if direction == 'DOWN': snake_position[1] += 10
    if direction == 'LEFT': snake_position[0] -= 10
    if direction == 'RIGHT': snake_position[0] += 10

    snake_body.insert(0, list(snake_position))

    if snake_position == fruit_position:
        score += 10
        foods_eaten += 1
        fruit_spawn = False
        if foods_eaten % 3 == 0:
            level += 1
            snake_speed += 2
            obstacles.extend(generate_obstacles(level))
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = spawn_fruit()
        fruit_spawn = True

    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
    for obs in obstacles:
        pygame.draw.rect(game_window, gray, pygame.Rect(obs[0], obs[1], 10, 10))

    
    if (snake_position[0] < 0 or snake_position[0] >= window_x or
        snake_position[1] < 0 or snake_position[1] >= window_y):
        game_over()
    for block in snake_body[1:]:
        if snake_position == block:
            game_over()
    for obs in obstacles:
        if snake_position == obs:
            game_over()

    show_score()
    pygame.display.update()
    fps.tick(snake_speed)
