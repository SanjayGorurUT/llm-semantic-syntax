import json
from testing.evaluator import evaluate_code, generate_summary
from prompts.templates import get_prompt

def example_evaluate_code():
    game_name = 'tic_tac_toe'
    prompt = get_prompt(game_name)
    
    print("Example prompt:")
    print(prompt[:200] + "...\n")
    
    example_code = """
import pygame
import sys

WIDTH = 600
HEIGHT = 600
board = [[None for _ in range(3)] for _ in range(3)]

def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True
    return False
"""
    
    print("Evaluating example code...")
    results = evaluate_code(example_code, game_name, runtime_iterations=5)
    summary = generate_summary(results)
    
    print(f"Syntax: {'PASS' if summary['syntax_passed'] else 'FAIL'}")
    print(f"Runtime: {'PASS' if summary['runtime_passed'] else 'FAIL'}")
    print(f"Semantic: {'PASS' if summary['semantic_passed'] else 'FAIL'}")
    
    return results, summary

if __name__ == '__main__':
    example_evaluate_code()

