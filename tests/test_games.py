import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_tic_tac_toe_import():
    from games import tic_tac_toe
    assert hasattr(tic_tac_toe, 'run_game')

def test_connect_four_import():
    from games import connect_four
    assert hasattr(connect_four, 'run_game')

def test_snakes_and_ladders_import():
    from games import snakes_and_ladders
    assert hasattr(snakes_and_ladders, 'run_game')

def test_snake_game_import():
    from games import snake_game
    assert hasattr(snake_game, 'run_game')

def test_ball_bouncing_import():
    from games import ball_bouncing
    assert hasattr(ball_bouncing, 'run_game')

def test_tic_tac_toe_syntax():
    from games import tic_tac_toe
    import ast
    with open('games/tic_tac_toe.py', 'r') as f:
        code = f.read()
    try:
        ast.parse(code)
        assert True
    except SyntaxError:
        pytest.fail("Tic-tac-toe has syntax errors")

def test_connect_four_syntax():
    from games import connect_four
    import ast
    with open('games/connect_four.py', 'r') as f:
        code = f.read()
    try:
        ast.parse(code)
        assert True
    except SyntaxError:
        pytest.fail("Connect Four has syntax errors")

def test_snake_game_syntax():
    from games import snake_game
    import ast
    with open('games/snake_game.py', 'r') as f:
        code = f.read()
    try:
        ast.parse(code)
        assert True
    except SyntaxError:
        pytest.fail("Snake game has syntax errors")

def test_ball_bouncing_syntax():
    from games import ball_bouncing
    import ast
    with open('games/ball_bouncing.py', 'r') as f:
        code = f.read()
    try:
        ast.parse(code)
        assert True
    except SyntaxError:
        pytest.fail("Ball bouncing has syntax errors")

def test_snakes_and_ladders_syntax():
    from games import snakes_and_ladders
    import ast
    with open('games/snakes_and_ladders.py', 'r') as f:
        code = f.read()
    try:
        ast.parse(code)
        assert True
    except SyntaxError:
        pytest.fail("Snakes and Ladders has syntax errors")

