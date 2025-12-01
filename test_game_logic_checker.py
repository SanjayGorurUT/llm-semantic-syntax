#!/usr/bin/env python3
"""
Test script to verify the game logic checker works correctly.
Tests the checker against reference game implementations.
"""

import os
import sys

# Set up headless pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from testing.game_logic_checker import test_game_logic_headless

GAMES = ['tic_tac_toe', 'connect_four', 'snake_game', 'ball_bouncing', 'snakes_and_ladders']

def test_game_logic_checker():
    """Test the game logic checker with reference implementations"""
    print("="*70)
    print("TESTING GAME LOGIC CHECKER")
    print("="*70)
    print()
    
    results = {}
    
    for game in GAMES:
        game_file = f"games/{game}.py"
        if not os.path.exists(game_file):
            print(f"⚠️  {game}: Reference file not found ({game_file})")
            results[game] = (False, "Reference file not found")
            continue
        
        print(f"Testing {game}...", end=" ", flush=True)
        
        try:
            with open(game_file, 'r') as f:
                code = f.read()
            
            passed, error = test_game_logic_headless(code, game)
            results[game] = (passed, error)
            
            if passed:
                print("✓ PASSED")
            else:
                print(f"✗ FAILED: {error}")
        
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            results[game] = (False, str(e))
        
        print()
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    
    passed_count = sum(1 for r in results.values() if r[0])
    total_count = len(results)
    
    for game, (passed, error) in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{game:20s} {status}")
        if not passed and error:
            print(f"  Error: {error}")
    
    print()
    print(f"Total: {passed_count}/{total_count} games passed")
    
    if passed_count == total_count:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(test_game_logic_checker())

