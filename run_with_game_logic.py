import json
import os
import ast
import time
import sys

sys.path.insert(0, os.path.dirname(__file__))
from testing.game_logic_checker import test_game_logic_headless
from prompts.templates import get_prompt

os.environ['GEMINI_API_KEY'] = "AIzaSyD_1pSTy7EohE7zMz_qEGoYlCl4V2buZFQ"
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

GAMES = ['tic_tac_toe', 'connect_four', 'snake_game', 'ball_bouncing', 'snakes_and_ladders']
REPETITIONS = 10
TEMPERATURE = 0.75

def call_gemini(prompt):
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt, generation_config={'temperature': TEMPERATURE})
        return response.text
    except Exception as e:
        return None

def extract_code(text):
    if "```python" in text:
        start = text.find("```python") + 9
        end = text.find("```", start)
        return text[start:end].strip()
    elif "```" in text:
        start = text.find("```") + 3
        end = text.find("```", start)
        return text[start:end].strip()
    return text.strip()

def check_syntax(code):
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Parse error: {str(e)}"

def check_semantic_simple(code, game_name):
    code_lower = code.lower()
    
    if game_name == 'tic_tac_toe':
        has_board = 'board' in code_lower or 'grid' in code_lower
        has_win = 'win' in code_lower or 'check' in code_lower
        has_pygame = 'pygame' in code_lower
        return has_board and has_win and has_pygame, None
    
    elif game_name == 'connect_four':
        has_board = 'board' in code_lower
        has_drop = 'drop' in code_lower or 'column' in code_lower
        has_pygame = 'pygame' in code_lower
        return has_board and has_drop and has_pygame, None
    
    elif game_name == 'snake_game':
        has_snake = 'snake' in code_lower
        has_fruit = 'fruit' in code_lower or 'food' in code_lower
        has_move = 'move' in code_lower or 'direction' in code_lower
        return has_snake and (has_fruit or has_move), None
    
    elif game_name == 'ball_bouncing':
        has_ball = 'ball' in code_lower
        has_bounce = 'bounce' in code_lower or 'collision' in code_lower
        has_velocity = 'velocity' in code_lower or 'speed' in code_lower
        return has_ball and (has_bounce or has_velocity), None
    
    elif game_name == 'snakes_and_ladders':
        has_ladder = 'ladder' in code_lower
        has_snake = 'snake' in code_lower
        has_position = 'position' in code_lower or 'pos' in code_lower
        return (has_ladder or has_snake) and has_position, None
    
    return False, "Unknown game"

results = {}
output_file = f"experiment_results_with_logic_{int(time.time())}.json"

print("="*70)
print("FULL EXPERIMENT - Syntax, Semantic & Game Logic")
print("="*70)
print(f"Games: {len(GAMES)}")
print(f"Repetitions: {REPETITIONS}")
print(f"Output: {output_file}")
print("="*70)
print()

for game_idx, game in enumerate(GAMES, 1):
    print(f"[{game_idx}/{len(GAMES)}] {game}")
    print("-" * 70)
    results[game] = {'gemini': []}
    
    prompt = get_prompt(game)
    
    for rep in range(REPETITIONS):
        print(f"  Rep {rep+1}/{REPETITIONS}... ", end="", flush=True)
        
        response = call_gemini(prompt)
        if response is None:
            print("API FAILED")
            results[game]['gemini'].append({
                'syntax_passed': False,
                'semantic_passed': False,
                'game_logic_passed': False,
                'error': 'API call failed'
            })
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            continue
        
        code = extract_code(response)
        if len(code) < 100:
            print("CODE TOO SHORT")
            results[game]['gemini'].append({
                'syntax_passed': False,
                'semantic_passed': False,
                'game_logic_passed': False,
                'error': 'Code too short'
            })
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            continue
        
        syntax_ok, syntax_err = check_syntax(code)
        semantic_ok, semantic_err = check_semantic_simple(code, game)
        
        game_logic_ok = False
        game_logic_err = None
        if syntax_ok:
            game_logic_ok, game_logic_err = test_game_logic_headless(code, game)
        
        syn_str = "✓" if syntax_ok else "✗"
        sem_str = "✓" if semantic_ok else "✗"
        logic_str = "✓" if game_logic_ok else "✗"
        print(f"Syntax:{syn_str} Semantic:{sem_str} Logic:{logic_str}")
        
        results[game]['gemini'].append({
            'syntax_passed': syntax_ok,
            'semantic_passed': semantic_ok,
            'game_logic_passed': game_logic_ok,
            'code_length': len(code),
            'syntax_error': syntax_err if not syntax_ok else None,
            'semantic_error': semantic_err if not semantic_ok else None,
            'game_logic_error': game_logic_err if not game_logic_ok else None
        })
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        time.sleep(2)
    
    syn_count = sum(1 for r in results[game]['gemini'] if r.get('syntax_passed', False))
    sem_count = sum(1 for r in results[game]['gemini'] if r.get('semantic_passed', False))
    logic_count = sum(1 for r in results[game]['gemini'] if r.get('game_logic_passed', False))
    print(f"  Summary: Syntax {syn_count}/{REPETITIONS}, Semantic {sem_count}/{REPETITIONS}, Logic {logic_count}/{REPETITIONS}\n")

print("="*70)
print("EXPERIMENT COMPLETE")
print("="*70)
print(f"Results: {output_file}")

matrix = {}
for game in GAMES:
    matrix[game] = {}
    matrix[game]['gemini'] = {
        'syntax': sum(1 for r in results[game]['gemini'] if r.get('syntax_passed', False)),
        'semantic': sum(1 for r in results[game]['gemini'] if r.get('semantic_passed', False)),
        'game_logic': sum(1 for r in results[game]['gemini'] if r.get('game_logic_passed', False))
    }

with open("results_matrix.json", 'w') as f:
    json.dump(matrix, f, indent=2)

print("Matrix: results_matrix.json")
print("\nFinal Summary:")
for game, data in matrix.items():
    print(f"  {game}:")
    print(f"    Syntax: {data['gemini']['syntax']}/{REPETITIONS}")
    print(f"    Semantic: {data['gemini']['semantic']}/{REPETITIONS}")
    print(f"    Game Logic: {data['gemini']['game_logic']}/{REPETITIONS}")

