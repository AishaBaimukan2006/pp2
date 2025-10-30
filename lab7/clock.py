import pygame
import datetime
from sys import exit

pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption("Clock")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None,50)
mike = pygame.image.load("C:/Users/Aisha/Desktop/pp2/lab7/image/49c5c19e-bd11-407d-bd7c-d3f17a2c6ad6.jpeg")
mike = pygame.transform.scale(mike, (700, 500))
mike_lefthand=pygame.image.load("C:/Users/Aisha/Desktop/pp2/lab7/image/dab16ac4-4eb9-4970-adda-3a2284aaa2b3.jpeg").convert_alpha()
mike_righthand=pygame.image.load("C:/Users/Aisha/Desktop/pp2/lab7/image/ff3ed679-6236-49da-944f-be965fcf3a53.jpeg").convert_alpha()

RED = (255, 0, 0)
black = (50,50,5)
clock_center=(350,262)

def rotate_image(image, angle, center):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=center)
    return rotated_image, new_rect

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    now=datetime.datetime.now()
    seconds = now.second + now.microsecond / 1_000_000 
    minutes = now.minute + seconds / 60
    second_angle = -seconds * 6
    minute_angle = -minutes * 6 
    time = datetime.datetime.now().strftime('%M:%S')
    text_surface = test_font.render(time,True,'Pink')
    text_rec = text_surface.get_rect(topleft = (0,0))
    
    screen.blit(mike,(0,0))  
    pygame.draw.circle(screen, black, (350,262), 15)
    rotated_second, second_rect = rotate_image(mike_lefthand, second_angle, clock_center)
    rotated_minute, minute_rect = rotate_image(mike_righthand, minute_angle, clock_center)
    screen.blit(rotated_minute, minute_rect.topleft)
    screen.blit(rotated_second, second_rect.topleft)
    pygame.draw.rect(screen,'black',text_rec,0,25)
    screen.blit(text_surface,text_rec)
    pygame.display.update()
    clock.tick(60)