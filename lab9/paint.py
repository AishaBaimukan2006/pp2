rectangle_width = 100
rectangle_height = 40
rectangle_x = WIDTH // 2 - rectangle_width // 2
rectangle_y = 50
rectangle_speed = 4
import pygame
from sys import exit

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Paint ")
clock = pygame.time.Clock()

color_mode = 'blue'
radius = 9
mode = 'pen'
drawing = False
prev_mode = 'pen'
points = []

screen.fill(pygame.Color('white'))

def get_color(color_mode):
    if color_mode == 'blue': return (0, 0, 255)
    elif color_mode == 'red': return (255, 0, 0)
    elif color_mode == 'green': return (0, 255, 0)
    elif color_mode == 'yellow': return (255, 255, 0)
    elif color_mode == 'black': return (0, 0, 0)
    return (0, 0, 0)


def draw_line(screen, start, end, width, color_mode):
    color = get_color(color_mode)
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    step = max(abs(dx), abs(dy))
    if step == 0:
        return
    for i in range(step):
        t = i / step
        x = int(start[0] * (1 - t) + end[0] * t)
        y = int(start[1] * (1 - t) + end[1] * t)
        pygame.draw.circle(screen, color, (x, y), width)



# RECTANGLE

def draw_rect(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
    pygame.draw.rect(screen, get_color(color), rect, width)



# CIRCLE

def draw_circle(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    r = int((((x2 - x1)**2 + (y2 - y1)**2)**0.5) / 2)
    center = ((x1 + x2) // 2, (y1 + y2) // 2)
    pygame.draw.circle(screen, get_color(color), center, r, width)



# квадрат

def draw_square(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))
    rect = pygame.Rect(min(x1, x2), min(y1, y2), side, side)
    pygame.draw.rect(screen, get_color(color), rect, width)


# тік бұрышты үшбұрыш

def draw_right_triangle(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(screen, get_color(color), points, width)



# шаршы

def draw_equilateral_triangle(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    side = abs(x2 - x1)

    p1 = (x1, y2)
    p2 = (x1 + side, y2)
    p3 = (x1 + side // 2, y2 - int(side * 0.866))  

    pygame.draw.polygon(screen, get_color(color), [p1, p2, p3], width)



# ромб

def draw_rhombus(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    dx = abs(x2 - x1) // 2
    dy = abs(y2 - y1) // 2

    points = [
        (cx, y1),     # top
        (x2, cy),     # right
        (cx, y2),     # bottom
        (x1, cy)      # left
    ]

    pygame.draw.polygon(screen, get_color(color), points, width)



FPS = 90

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

        # клавиратура
        if e.type == pygame.KEYDOWN:

            # шығу
            if e.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            #пішіндер
            if e.key == pygame.K_p: mode = 'pen'
            if e.key == pygame.K_r: mode = 'rectangle'
            if e.key == pygame.K_c: mode = 'circle'
            if e.key == pygame.K_s: mode = 'square'
            if e.key == pygame.K_t: mode = 'right_triangle'
            if e.key == pygame.K_q: mode = 'equilateral_triangle'
            if e.key == pygame.K_h: mode = 'rhombus'

            # ластик
            if e.key == pygame.K_e:
                if mode != 'erase':
                    prev_mode = mode
                    mode = 'erase'
                else:
                    mode = prev_mode

            # түс
            if e.key == pygame.K_1: color_mode = 'blue'
            if e.key == pygame.K_2: color_mode = 'red'
            if e.key == pygame.K_3: color_mode = 'green'
            if e.key == pygame.K_4: color_mode = 'yellow'
            if e.key == pygame.K_5: color_mode = 'black'

            
            if e.key == pygame.K_0:
                screen.fill(pygame.Color('white'))

            
            if e.key == pygame.K_UP: radius = min(200, radius + 1)
            if e.key == pygame.K_DOWN: radius = max(1, radius - 1)

        
        if e.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = e.pos
            points = [start_pos]

        elif e.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = e.pos

            if mode == 'rectangle': draw_rect(screen, start_pos, end_pos, radius, color_mode)
            elif mode == 'circle': draw_circle(screen, start_pos, end_pos, radius, color_mode)
            elif mode == 'square': draw_square(screen, start_pos, end_pos, radius, color_mode)
            elif mode == 'right_triangle': draw_right_triangle(screen, start_pos, end_pos, radius, color_mode)
            elif mode == 'equilateral_triangle': draw_equilateral_triangle(screen, start_pos, end_pos, radius, color_mode)
            elif mode == 'rhombus': draw_rhombus(screen, start_pos, end_pos, radius, color_mode)

        elif e.type == pygame.MOUSEMOTION and drawing:
            if mode == 'pen':
                pos = e.pos
                points.append(pos)
                if len(points) > 1:
                    draw_line(screen, points[-2], points[-1], radius, color_mode)

            elif mode == 'erase':
                pygame.draw.circle(screen, pygame.Color('white'), e.pos, radius)

    pygame.display.flip()
    clock.tick(FPS)
