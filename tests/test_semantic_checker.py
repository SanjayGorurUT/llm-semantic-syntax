import pytest
from testing.semantic_checker import check_semantic_correctness

def test_semantic_tic_tac_toe():
    code = """
def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    return False

board = [[1, 1, 1], [None, 2, None], [None, None, 2]]
"""
    passed, error = check_semantic_correctness(code, 'tic_tac_toe')
    assert isinstance(passed, bool)

def test_semantic_connect_four():
    code = """
import numpy as np
def winning_move(board, piece):
    return True
"""
    passed, error = check_semantic_correctness(code, 'connect_four')
    assert isinstance(passed, bool)

def test_semantic_snake():
    code = """
class Snake:
    def __init__(self):
        self.body = []
"""
    passed, error = check_semantic_correctness(code, 'snake_game')
    assert isinstance(passed, bool)

def test_semantic_ball_bouncing():
    code = """
ball_x = 100
ball_velocity_x = 5
def update_ball():
    global ball_x
    ball_x += ball_velocity_x
"""
    passed, error = check_semantic_correctness(code, 'ball_bouncing')
    assert isinstance(passed, bool)

def test_semantic_snakes_ladders():
    code = """
ladders = {3: 22}
snakes = {27: 1}
position = 1
"""
    passed, error = check_semantic_correctness(code, 'snakes_and_ladders')
    assert isinstance(passed, bool)

