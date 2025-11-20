import pygame
import time
import random
import sys

pygame.init()

window_x = 1000
window_y = 500

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
gray = pygame.Color(100, 100, 100)

pygame.display.set_caption('Snake Game ')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()


# экранға текст шығаратын функция
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():
    menu_font = pygame.font.SysFont('times new roman', 50)
    while True:
        game_window.fill(black)
        draw_text('Snake Game', menu_font, white, game_window, window_x//2, window_y//2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return



def game_over_screen(score, level):
    while True:
        game_window.fill(black)
        draw_text(f'Ваш счёт: {score}', pygame.font.SysFont('times new roman', 40), red,
                  game_window, window_x//2, window_y//3)
        draw_text(f'Уровень: {level}', pygame.font.SysFont('times new roman', 30), white,
                  game_window, window_x//2, window_y//2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return True


def game():
    snake_speed = 10
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

    # жемісті кездейсоқ шығаратын функция
    def spawn_fruit():
        while True:
            new_fruit = [
                random.randrange(1, (window_x // 10)) * 10,
                random.randrange(1, (window_y // 10)) * 10
            ]
            if new_fruit not in snake_body:
                return new_fruit

   
    fruit_position = spawn_fruit()
    fruit_spawn = True

  
    fruit_weight = random.choice([1, 2, 3])

    # жемістің өмір сүру уақыты 
    fruit_timer = 200  

    direction = 'RIGHT'
    change_to = direction
    score = 0
    level = 1
    foods_eaten = 0
    obstacles = []

    # кедергілер генерациясы
    def generate_obstacles(level):
        new_obstacles = []
        for _ in range(level * 3):
            x = random.randrange(0, window_x // 10) * 10
            y = random.randrange(0, window_y // 10) * 10
            new_obstacles.append([x, y])
        return new_obstacles

    # экранға балл мен деңгейді шығару
    def show_score(color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render(
            f'Счет: {score}  Уровень: {level}', True, color)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (10, 10)
        game_window.blit(score_surface, score_rect)

    while True:
        # басқару
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

        # бағыты
        if change_to == 'UP':
            direction = 'UP'
        if change_to == 'DOWN':
            direction = 'DOWN'
        if change_to == 'LEFT':
            direction = 'LEFT'
        if change_to == 'RIGHT':
            direction = 'RIGHT'

        # жылжу
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        snake_body.insert(0, list(snake_position))

        # егер жеміс жеген болса
        if snake_position == fruit_position:
            score += 10 * fruit_weight   # салмаққа байланысты көп қосылады
            foods_eaten += 1
            fruit_spawn = False

            # әр 3 жеміс сайын деңгей өседі
            if foods_eaten % 3 == 0:
                level += 1
                snake_speed += 2
                obstacles.extend(generate_obstacles(level))
        else:
            snake_body.pop()

        # жеміс spawn + weight + timer reset
        if not fruit_spawn:
            fruit_position = spawn_fruit()
            fruit_weight = random.choice([1, 2, 3])  # жаңа салмақ
            fruit_timer = 200                       # таймерді жаңарту
        fruit_spawn = True

        # жемістуақыт біткенде жоғалады
        fruit_timer -= 1
        if fruit_timer <= 0:
            fruit_position = spawn_fruit()          # жаңадан шығару
            fruit_weight = random.choice([1, 2, 3]) # жаңа салмақ
            fruit_timer = 200                       # таймерді қайта қосу

   
        game_window.fill(black)

       
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # жеміс 
        fruit_color = white if fruit_weight == 1 else (0, 200, 255) if fruit_weight == 2 else (255, 215, 0)
        pygame.draw.rect(game_window, fruit_color,
                         pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        # кедергілер
        for obs in obstacles:
            pygame.draw.rect(game_window, gray, pygame.Rect(obs[0], obs[1], 10, 10))

        # шекарамен
        if snake_position[0] < 0 or snake_position[0] > window_x - 10:
            if game_over_screen(score, level):
                return
        if snake_position[1] < 0 or snake_position[1] > window_y - 10:
            if game_over_screen(score, level):
                return

        # өзине тию
        for block in snake_body[1:]:
            if snake_position == block:
                if game_over_screen(score, level):
                    return

        # кедергімен 
        for obs in obstacles:
            if snake_position == obs:
                if game_over_screen(score, level):
                    return

        show_score(blue, 'times new roman', 35)
        pygame.display.update()
        fps.tick(snake_speed)

while True:
    main_menu()
    game()

