TIC_TAC_TOE_PROMPT = """Create a complete Python game using pygame for Tic-Tac-Toe.

Rules:
- 3x3 grid board
- Two players alternate turns (Player 1 uses circles, Player 2 uses crosses)
- Players click on empty squares to place their mark
- First player to get 3 marks in a row (horizontal, vertical, or diagonal) wins
- If all squares are filled with no winner, it's a tie
- Press 'R' to restart the game

Requirements:
- Use Python and pygame library
- Window size: 600x600 pixels
- Implement the game loop with event handling
- Draw the board with lines
- Handle mouse clicks to place marks
- Check for win conditions after each move
- Display winning line when game ends
- Handle game restart functionality

Write the complete, runnable code."""

CONNECT_FOUR_PROMPT = """Create a complete Python game using pygame for Connect Four.

Rules:
- 6 rows x 7 columns board
- Two players alternate dropping pieces (Player 1: red, Player 2: yellow)
- Pieces fall to the lowest available row in the selected column
- First player to get 4 pieces in a row (horizontal, vertical, or diagonal) wins
- Click on a column to drop a piece

Requirements:
- Use Python, pygame, and numpy libraries
- Window size: 700x700 pixels (7 columns * 100px, 6 rows * 100px + header)
- Implement the game loop with event handling
- Draw the board with circles
- Handle mouse clicks to select column
- Check for valid column and available row
- Check for win conditions after each move
- Display winner when game ends

Write the complete, runnable code."""

SNAKES_AND_LADDERS_PROMPT = """Create a complete Python game using pygame for Snakes and Ladders.

Rules:
- 10x10 board (100 squares total)
- Player starts at position 1
- Press SPACE to roll a 6-sided die and move forward
- If player lands on a ladder bottom, move to ladder top
- If player lands on a snake head, move to snake tail
- Win by reaching position 100
- Press 'R' to restart

Ladders: 3->22, 5->8, 11->26, 20->29, 17->4
Snakes: 27->1, 21->9, 19->7, 25->13, 15->6

Requirements:
- Use Python and pygame library
- Window size: 600x600 pixels
- Implement the game loop with event handling
- Draw the board with numbered squares
- Draw ladders and snakes visually
- Handle dice rolling and movement
- Check for ladder/snake collisions
- Display current position and dice value
- Handle game restart functionality

Write the complete, runnable code."""

SNAKE_GAME_PROMPT = """Create a complete Python game using pygame for Snake.

Rules:
- Snake starts with 3 segments, moving right
- Use arrow keys to change direction (up, down, left, right)
- Snake cannot reverse into itself
- When snake eats fruit (red square), it grows by one segment
- Game ends if snake hits wall or itself
- Score increases by 1 for each fruit eaten
- Game restarts automatically on collision

Requirements:
- Use Python and pygame library
- Window size: 600x600 pixels
- Cell size: 20x20 pixels (30x30 grid)
- Implement the game loop with event handling
- Draw snake as green rectangles
- Draw fruit as red square
- Handle keyboard input for direction
- Update snake position continuously
- Check for collisions (walls and self)
- Display score
- Handle game restart on collision

Write the complete, runnable code."""

BALL_BOUNCING_PROMPT = """Create a complete Python game using pygame for Ball Bouncing.

Rules:
- Red ball moves continuously in a window
- Ball bounces off all four walls
- Ball maintains velocity when bouncing
- Ball should not go outside window boundaries
- Press 'R' to reset ball to center

Requirements:
- Use Python and pygame library
- Window size: 800x600 pixels
- Ball radius: 20 pixels
- Ball color: red
- Background: black
- Implement the game loop
- Update ball position each frame
- Check for wall collisions and reverse velocity
- Keep ball within window bounds
- Handle reset functionality

Write the complete, runnable code."""

GAME_PROMPTS = {
    'tic_tac_toe': TIC_TAC_TOE_PROMPT,
    'connect_four': CONNECT_FOUR_PROMPT,
    'snakes_and_ladders': SNAKES_AND_LADDERS_PROMPT,
    'snake_game': SNAKE_GAME_PROMPT,
    'ball_bouncing': BALL_BOUNCING_PROMPT
}

def get_prompt(game_name):
    return GAME_PROMPTS.get(game_name, "")

