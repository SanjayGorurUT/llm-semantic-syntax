import importlib.util
import tempfile
import os
import sys

def load_code_as_module(code_string, module_name="test_module"):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code_string)
        temp_file = f.name
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, temp_file)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        return None
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass

def check_game_logic_tic_tac_toe(code_string):
    module = load_code_as_module(code_string, "ttt_test")
    if module is None:
        return False, "Failed to load module"
    
    try:
        if not hasattr(module, 'check_win'):
            return False, "Missing check_win function"
        
        test_board = [[1, 1, 1], [None, 2, None], [None, None, 2]]
        result = module.check_win(test_board, 1)
        if not result:
            return False, "Win detection failed"
        
        return True, None
    except Exception as e:
        return False, f"Logic error: {str(e)}"

def check_game_logic_connect_four(code_string):
    module = load_code_as_module(code_string, "c4_test")
    if module is None:
        return False, "Failed to load module"
    
    try:
        if hasattr(module, 'winning_move'):
            import numpy as np
            test_board = np.zeros((6, 7))
            test_board[0][0] = 1
            test_board[1][0] = 1
            test_board[2][0] = 1
            test_board[3][0] = 1
            result = module.winning_move(test_board, 1)
            if not result:
                return False, "Win detection failed"
        
        return True, None
    except Exception as e:
        return False, f"Logic error: {str(e)}"

def check_game_logic_snake(code_string):
    module = load_code_as_module(code_string, "snake_test")
    if module is None:
        return False, "Failed to load module"
    
    try:
        if hasattr(module, 'Snake') or hasattr(module, 'snake'):
            return True, None
        return False, "Missing Snake class or logic"
    except Exception as e:
        return False, f"Logic error: {str(e)}"

def check_game_logic_ball_bouncing(code_string):
    module = load_code_as_module(code_string, "ball_test")
    if module is None:
        return False, "Failed to load module"
    
    try:
        has_ball = hasattr(module, 'ball_x') or hasattr(module, 'ball_velocity_x')
        has_update = 'update' in code_string.lower() or 'move' in code_string.lower()
        if has_ball or has_update:
            return True, None
        return False, "Missing ball physics logic"
    except Exception as e:
        return False, f"Logic error: {str(e)}"

def check_game_logic_snakes_ladders(code_string):
    module = load_code_as_module(code_string, "sl_test")
    if module is None:
        return False, "Failed to load module"
    
    try:
        has_ladders = 'ladder' in code_string.lower()
        has_snakes = 'snake' in code_string.lower()
        has_position = 'position' in code_string.lower() or 'pos' in code_string.lower()
        if has_ladders and has_snakes and has_position:
            return True, None
        return False, "Missing game mechanics"
    except Exception as e:
        return False, f"Logic error: {str(e)}"

GAME_LOGIC_CHECKERS = {
    'tic_tac_toe': check_game_logic_tic_tac_toe,
    'connect_four': check_game_logic_connect_four,
    'snake_game': check_game_logic_snake,
    'ball_bouncing': check_game_logic_ball_bouncing,
    'snakes_and_ladders': check_game_logic_snakes_ladders
}

def check_semantic_correctness(code_string, game_name):
    if game_name not in GAME_LOGIC_CHECKERS:
        return False, f"Unknown game: {game_name}"
    
    checker = GAME_LOGIC_CHECKERS[game_name]
    return checker(code_string)

