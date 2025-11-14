import pytest
from prompts.templates import get_prompt, GAME_PROMPTS

def test_get_prompt_tic_tac_toe():
    prompt = get_prompt('tic_tac_toe')
    assert len(prompt) > 0
    assert 'Tic-Tac-Toe' in prompt or 'tic-tac-toe' in prompt.lower()

def test_get_prompt_connect_four():
    prompt = get_prompt('connect_four')
    assert len(prompt) > 0
    assert 'Connect Four' in prompt or 'connect four' in prompt.lower()

def test_get_prompt_snake_game():
    prompt = get_prompt('snake_game')
    assert len(prompt) > 0
    assert 'Snake' in prompt or 'snake' in prompt.lower()

def test_get_prompt_ball_bouncing():
    prompt = get_prompt('ball_bouncing')
    assert len(prompt) > 0
    assert 'Ball' in prompt or 'ball' in prompt.lower()

def test_get_prompt_snakes_and_ladders():
    prompt = get_prompt('snakes_and_ladders')
    assert len(prompt) > 0

def test_get_prompt_invalid():
    prompt = get_prompt('invalid_game')
    assert prompt == ""

def test_all_games_have_prompts():
    assert len(GAME_PROMPTS) >= 5
    assert 'tic_tac_toe' in GAME_PROMPTS
    assert 'connect_four' in GAME_PROMPTS
    assert 'snake_game' in GAME_PROMPTS
    assert 'ball_bouncing' in GAME_PROMPTS
    assert 'snakes_and_ladders' in GAME_PROMPTS

