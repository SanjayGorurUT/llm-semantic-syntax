import pytest
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.mark.skipif(os.getenv('SKIP_PLAY_TESTS') == '1', reason='Skip interactive game tests')
def test_play_tic_tac_toe():
    from games import tic_tac_toe
    import pygame
    pygame.init()
    pygame.quit()
    assert True

@pytest.mark.skipif(os.getenv('SKIP_PLAY_TESTS') == '1', reason='Skip interactive game tests')
def test_play_connect_four():
    from games import connect_four
    import pygame
    pygame.init()
    pygame.quit()
    assert True

@pytest.mark.skipif(os.getenv('SKIP_PLAY_TESTS') == '1', reason='Skip interactive game tests')
def test_play_snake_game():
    from games import snake_game
    import pygame
    pygame.init()
    pygame.quit()
    assert True

@pytest.mark.skipif(os.getenv('SKIP_PLAY_TESTS') == '1', reason='Skip interactive game tests')
def test_play_ball_bouncing():
    from games import ball_bouncing
    import pygame
    pygame.init()
    pygame.quit()
    assert True

@pytest.mark.skipif(os.getenv('SKIP_PLAY_TESTS') == '1', reason='Skip interactive game tests')
def test_play_snakes_and_ladders():
    from games import snakes_and_ladders
    import pygame
    pygame.init()
    pygame.quit()
    assert True

