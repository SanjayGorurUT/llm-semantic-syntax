import pygame
import sys
import math

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Ball Bouncing')
clock = pygame.time.Clock()

ball_radius = 20
ball_x = WINDOW_WIDTH // 2
ball_y = WINDOW_HEIGHT // 2
ball_velocity_x = 5
ball_velocity_y = 5

def draw_ball():
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

def update_ball():
    global ball_x, ball_y, ball_velocity_x, ball_velocity_y
    
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y
    
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WINDOW_WIDTH:
        ball_velocity_x = -ball_velocity_x
        if ball_x - ball_radius <= 0:
            ball_x = ball_radius
        else:
            ball_x = WINDOW_WIDTH - ball_radius
    
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= WINDOW_HEIGHT:
        ball_velocity_y = -ball_velocity_y
        if ball_y - ball_radius <= 0:
            ball_y = ball_radius
        else:
            ball_y = WINDOW_HEIGHT - ball_radius

def run_game():
    global ball_x, ball_y, ball_velocity_x, ball_velocity_y
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    ball_x = WINDOW_WIDTH // 2
                    ball_y = WINDOW_HEIGHT // 2
                    ball_velocity_x = 5
                    ball_velocity_y = 5
        
        screen.fill(BLACK)
        update_ball()
        draw_ball()
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    run_game()

