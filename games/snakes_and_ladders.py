import pygame
import sys
import random

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
BOARD_SIZE = 10
CELL_SIZE = WINDOW_WIDTH // BOARD_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

ladders = {3: 22, 5: 8, 11: 26, 20: 29, 17: 4}
snakes = {27: 1, 21: 9, 19: 7, 25: 13, 15: 6}

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snakes and Ladders')
clock = pygame.time.Clock()

player_pos = 1
dice_value = 0
game_over = False

def draw_board():
    screen.fill(WHITE)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            
            num = row * BOARD_SIZE + col + 1
            if row % 2 == 1:
                num = (row + 1) * BOARD_SIZE - col
            
            font = pygame.font.Font(None, 24)
            text = font.render(str(num), True, BLACK)
            text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            screen.blit(text, text_rect)
            
            if num in ladders:
                start_row = (num - 1) // BOARD_SIZE
                start_col = (num - 1) % BOARD_SIZE
                if start_row % 2 == 1:
                    start_col = BOARD_SIZE - 1 - start_col
                end_num = ladders[num]
                end_row = (end_num - 1) // BOARD_SIZE
                end_col = (end_num - 1) % BOARD_SIZE
                if end_row % 2 == 1:
                    end_col = BOARD_SIZE - 1 - end_col
                start_pos = (start_col * CELL_SIZE + CELL_SIZE // 2, start_row * CELL_SIZE + CELL_SIZE // 2)
                end_pos = (end_col * CELL_SIZE + CELL_SIZE // 2, end_row * CELL_SIZE + CELL_SIZE // 2)
                pygame.draw.line(screen, GREEN, start_pos, end_pos, 3)
            
            if num in snakes:
                start_row = (num - 1) // BOARD_SIZE
                start_col = (num - 1) % BOARD_SIZE
                if start_row % 2 == 1:
                    start_col = BOARD_SIZE - 1 - start_col
                end_num = snakes[num]
                end_row = (end_num - 1) // BOARD_SIZE
                end_col = (end_num - 1) % BOARD_SIZE
                if end_row % 2 == 1:
                    end_col = BOARD_SIZE - 1 - end_col
                start_pos = (start_col * CELL_SIZE + CELL_SIZE // 2, start_row * CELL_SIZE + CELL_SIZE // 2)
                end_pos = (end_col * CELL_SIZE + CELL_SIZE // 2, end_row * CELL_SIZE + CELL_SIZE // 2)
                pygame.draw.line(screen, RED, start_pos, end_pos, 3)

def get_position_coords(position):
    if position < 1 or position > BOARD_SIZE * BOARD_SIZE:
        return None
    row = (position - 1) // BOARD_SIZE
    col = (position - 1) % BOARD_SIZE
    if row % 2 == 1:
        col = BOARD_SIZE - 1 - col
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2
    return (x, y)

def draw_player():
    coords = get_position_coords(player_pos)
    if coords:
        pygame.draw.circle(screen, BLUE, coords, 15)

def roll_dice():
    return random.randint(1, 6)

def move_player(steps):
    global player_pos, game_over
    new_pos = player_pos + steps
    if new_pos <= BOARD_SIZE * BOARD_SIZE:
        player_pos = new_pos
        if player_pos in ladders:
            player_pos = ladders[player_pos]
        if player_pos in snakes:
            player_pos = snakes[player_pos]
        if player_pos >= BOARD_SIZE * BOARD_SIZE:
            player_pos = BOARD_SIZE * BOARD_SIZE
            game_over = True

def run_game():
    global player_pos, dice_value, game_over
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    dice_value = roll_dice()
                    move_player(dice_value)
                elif event.key == pygame.K_r:
                    player_pos = 1
                    game_over = False
                    dice_value = 0
        
        draw_board()
        draw_player()
        
        font = pygame.font.Font(None, 36)
        status_text = f"Position: {player_pos} | Dice: {dice_value}"
        if game_over:
            status_text = "You Win! Press R to restart"
        text = font.render(status_text, True, BLACK)
        screen.blit(text, (10, WINDOW_HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    run_game()

