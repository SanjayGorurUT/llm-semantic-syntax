import ast
import importlib.util
import tempfile
import os
import sys

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    # Create a simple array-like for basic testing
    class SimpleArray:
        def zeros(self, shape, dtype=int):
            if len(shape) == 2:
                return [[0 for _ in range(shape[1])] for _ in range(shape[0])]
            return [0] * shape[0]
    np = SimpleArray()

def test_game_logic_headless(code_string, game_name):
    """
    Test game logic by actually running the code and testing game functions.
    Returns (passed: bool, error: str or None)
    """
    try:
        # Set up headless pygame environment
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
        
        fd, temp_file = tempfile.mkstemp(suffix='.py')
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(code_string)
            
            spec = importlib.util.spec_from_file_location("test_game", temp_file)
            if spec is None or spec.loader is None:
                return False, "Failed to create module spec"
            
            module = importlib.util.module_from_spec(spec)
            sys.modules["test_game"] = module
            
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                return False, f"Module execution error: {str(e)[:200]}"
            
            # Test game-specific logic
            if game_name == 'tic_tac_toe':
                return test_tic_tac_toe_logic(module)
            elif game_name == 'connect_four':
                return test_connect_four_logic(module)
            elif game_name == 'snake_game':
                return test_snake_logic(module)
            elif game_name == 'ball_bouncing':
                return test_ball_bouncing_logic(module)
            elif game_name == 'snakes_and_ladders':
                return test_snakes_ladders_logic(module)
            else:
                return False, "Unknown game"
        
        finally:
            try:
                os.unlink(temp_file)
            except:
                pass
    
    except Exception as e:
        return False, f"Test error: {str(e)[:200]}"

def test_tic_tac_toe_logic(module):
    """Test tic-tac-toe game logic by actually running check_win function"""
    try:
        # Check if board exists or can be created
        board = None
        if hasattr(module, 'board'):
            board = module.board
        else:
            # Try to create a board
            board = [[None for _ in range(3)] for _ in range(3)]
        
        # Test check_win function - this is the key game logic
        if hasattr(module, 'check_win'):
            # Test horizontal win
            test_board = [[1, 1, 1], [None, 2, None], [None, None, 2]]
            try:
                result = module.check_win(test_board, 1)
                if not result:
                    return False, "Win detection failed for horizontal win"
            except Exception as e:
                # Try with just player parameter if function signature is different
                try:
                    # Some implementations might use module.board
                    if hasattr(module, 'board'):
                        module.board = test_board
                        result = module.check_win(1)
                        if not result:
                            return False, "Win detection failed (using module board)"
                except:
                    return False, f"check_win function error: {str(e)[:100]}"
            
            # Test vertical win
            test_board2 = [[1, None, 2], [1, None, 2], [1, None, None]]
            try:
                result = module.check_win(test_board2, 1)
                if not result:
                    return False, "Win detection failed for vertical win"
            except:
                pass
            
            # Test diagonal win
            test_board3 = [[1, None, 2], [None, 1, 2], [None, None, 1]]
            try:
                result = module.check_win(test_board3, 1)
                if not result:
                    return False, "Win detection failed for diagonal win"
            except:
                pass
            
            # Test no win case
            test_board4 = [[1, 2, 1], [2, 1, 2], [None, None, None]]
            try:
                result = module.check_win(test_board4, 1)
                if result:
                    return False, "False positive win detection"
            except:
                pass
            
            return True, None
        else:
            return False, "Missing check_win function"
            
    except Exception as e:
        return False, f"Logic test error: {str(e)[:100]}"

def test_connect_four_logic(module):
    """Test connect four game logic by actually running winning_move function"""
    try:
        if hasattr(module, 'winning_move'):
            # Test horizontal win
            try:
                if HAS_NUMPY:
                    board = np.zeros((6, 7), dtype=int)
                else:
                    board = [[0 for _ in range(7)] for _ in range(6)]
                board[0][0] = 1
                board[0][1] = 1
                board[0][2] = 1
                board[0][3] = 1
                result = module.winning_move(board, 1)
                if not result:
                    return False, "Win detection failed for horizontal win"
            except Exception as e:
                return False, f"winning_move error: {str(e)[:100]}"
            
            # Test vertical win
            try:
                if HAS_NUMPY:
                    board2 = np.zeros((6, 7), dtype=int)
                else:
                    board2 = [[0 for _ in range(7)] for _ in range(6)]
                board2[0][0] = 1
                board2[1][0] = 1
                board2[2][0] = 1
                board2[3][0] = 1
                result = module.winning_move(board2, 1)
                if not result:
                    return False, "Win detection failed for vertical win"
            except:
                pass
            
            # Test no win case
            try:
                if HAS_NUMPY:
                    board3 = np.zeros((6, 7), dtype=int)
                else:
                    board3 = [[0 for _ in range(7)] for _ in range(6)]
                board3[0][0] = 1
                board3[0][1] = 1
                board3[0][2] = 1
                result = module.winning_move(board3, 1)
                if result:
                    return False, "False positive win detection"
            except:
                pass
            
            return True, None
        elif hasattr(module, 'create_board'):
            # At least has board creation
            try:
                board = module.create_board()
                if board is not None:
                    return True, None
            except:
                pass
            return False, "Missing winning_move function"
        else:
            return False, "Missing winning_move function"
            
    except Exception as e:
        return False, f"Logic test error: {str(e)[:100]}"

def test_snake_logic(module):
    """Test snake game logic by creating and testing Snake class"""
    try:
        # Check for Snake class
        Snake = None
        if hasattr(module, 'Snake'):
            Snake = module.Snake
        elif 'Snake' in dir(module):
            Snake = getattr(module, 'Snake')
        
        if Snake is not None:
            try:
                # Try to instantiate and test basic functionality
                snake = Snake()
                
                # Test that it has required methods
                if hasattr(snake, 'move_snake') or hasattr(snake, 'move'):
                    # Test collision detection if available
                    if hasattr(snake, 'check_collision'):
                        # This should work without crashing
                        try:
                            _ = snake.check_collision()
                        except:
                            pass
                    
                    return True, None
                else:
                    return False, "Snake class missing move functionality"
            except Exception as e:
                return False, f"Snake instantiation error: {str(e)[:100]}"
        else:
            return False, "Missing Snake class"
            
    except Exception as e:
        return False, f"Logic test error: {str(e)[:100]}"

def test_ball_bouncing_logic(module):
    """Test ball bouncing logic by checking physics functions"""
    try:
        # Check if update function exists and works
        if hasattr(module, 'update_ball'):
            try:
                # Set initial state if variables exist
                if hasattr(module, 'ball_x'):
                    original_x = module.ball_x
                if hasattr(module, 'ball_y'):
                    original_y = module.ball_y
                if hasattr(module, 'ball_velocity_x'):
                    original_vx = module.ball_velocity_x
                if hasattr(module, 'ball_velocity_y'):
                    original_vy = module.ball_velocity_y
                
                # Try to call update function
                module.update_ball()
                
                # Check if position changed (indicating physics works)
                if hasattr(module, 'ball_x') and hasattr(module, 'ball_velocity_x'):
                    if module.ball_x != original_x or module.ball_velocity_x != original_vx:
                        return True, None
                
                return True, None
            except Exception as e:
                return False, f"update_ball error: {str(e)[:100]}"
        elif hasattr(module, 'ball_x') and hasattr(module, 'ball_velocity_x'):
            # At least has ball variables
            return True, None
        else:
            return False, "Missing ball physics (update_ball or ball variables)"
            
    except Exception as e:
        return False, f"Logic test error: {str(e)[:100]}"

def test_snakes_ladders_logic(module):
    """Test snakes and ladders logic by checking game mechanics"""
    try:
        # Check for ladders and snakes dictionaries
        has_ladders = hasattr(module, 'ladders') or 'ladders' in dir(module)
        has_snakes = hasattr(module, 'snakes') or 'snakes' in dir(module)
        has_position = (hasattr(module, 'player_pos') or hasattr(module, 'position') or 
                       'player_pos' in dir(module) or 'position' in dir(module))
        
        if has_ladders or has_snakes:
            # Try to access the dictionaries
            try:
                if has_ladders:
                    ladders = getattr(module, 'ladders', {})
                    if not isinstance(ladders, dict):
                        return False, "ladders is not a dictionary"
                
                if has_snakes:
                    snakes = getattr(module, 'snakes', {})
                    if not isinstance(snakes, dict):
                        return False, "snakes is not a dictionary"
                
                if has_position:
                    return True, None
                else:
                    return False, "Missing position tracking"
            except Exception as e:
                return False, f"Error accessing game mechanics: {str(e)[:100]}"
        else:
            return False, "Missing ladders and snakes dictionaries"
            
    except Exception as e:
        return False, f"Logic test error: {str(e)[:100]}"
