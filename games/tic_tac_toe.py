import pygame
import sys

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
player = 1
game_over = False
winner = None

def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def check_win(player):
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True
    return False

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, RED, (posX, 15), (posX, HEIGHT - 15), 15)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, RED, (15, posY), (WIDTH - 15, posY), 15)

def draw_asc_diagonal(player):
    pygame.draw.line(screen, RED, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)

def draw_desc_diagonal(player):
    pygame.draw.line(screen, RED, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)

def restart():
    global board, player, game_over, winner
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = 1
    game_over = False
    winner = None
    screen.fill(BG_COLOR)
    draw_lines()

def get_clicked_row_col(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    if row >= 0 and row < BOARD_ROWS and col >= 0 and col < BOARD_COLS:
        return (int(row), int(col))
    return None

def run_game():
    global player, game_over, winner
    draw_lines()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row_col = get_clicked_row_col((mouseX, mouseY))
                
                if clicked_row_col:
                    row, col = clicked_row_col
                    if available_square(row, col):
                        mark_square(row, col, player)
                        if check_win(player):
                            game_over = True
                            winner = player
                            if col == 0 and board[0][col] == player and board[1][col] == player and board[2][col] == player:
                                draw_vertical_winning_line(col, player)
                            elif col == 1 and board[0][col] == player and board[1][col] == player and board[2][col] == player:
                                draw_vertical_winning_line(col, player)
                            elif col == 2 and board[0][col] == player and board[1][col] == player and board[2][col] == player:
                                draw_vertical_winning_line(col, player)
                            elif row == 0 and board[row][0] == player and board[row][1] == player and board[row][2] == player:
                                draw_horizontal_winning_line(row, player)
                            elif row == 1 and board[row][0] == player and board[row][1] == player and board[row][2] == player:
                                draw_horizontal_winning_line(row, player)
                            elif row == 2 and board[row][0] == player and board[row][1] == player and board[row][2] == player:
                                draw_horizontal_winning_line(row, player)
                            elif board[0][0] == player and board[1][1] == player and board[2][2] == player:
                                draw_desc_diagonal(player)
                            elif board[2][0] == player and board[1][1] == player and board[0][2] == player:
                                draw_asc_diagonal(player)
                        elif is_board_full():
                            game_over = True
                            winner = None
                        else:
                            player = 2 if player == 1 else 1
                        draw_figures()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
        
        pygame.display.update()

if __name__ == '__main__':
    run_game()

