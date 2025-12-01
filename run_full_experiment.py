import json
import os
import ast
import time
import importlib.util
import tempfile
import sys

os.environ['GEMINI_API_KEY'] = "AIzaSyD_1pSTy7EohE7zMz_qEGoYlCl4V2buZFQ"

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

from prompts.templates import get_prompt

results = {}
output_file = f"experiment_results_full_{int(time.time())}.json"

print("="*70)
print("FULL EXPERIMENT - Syntax & Semantic (No Runtime)")
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
                'error': 'Code too short'
            })
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            continue
        
        syntax_ok, syntax_err = check_syntax(code)
        semantic_ok, semantic_err = check_semantic_simple(code, game)
        
        syn_str = "✓" if syntax_ok else "✗"
        sem_str = "✓" if semantic_ok else "✗"
        print(f"Syntax:{syn_str} Semantic:{sem_str}")
        
        results[game]['gemini'].append({
            'syntax_passed': syntax_ok,
            'semantic_passed': semantic_ok,
            'code_length': len(code),
            'syntax_error': syntax_err if not syntax_ok else None,
            'semantic_error': semantic_err if not semantic_ok else None
        })
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        time.sleep(2)
    
    syn_count = sum(1 for r in results[game]['gemini'] if r.get('syntax_passed', False))
    sem_count = sum(1 for r in results[game]['gemini'] if r.get('semantic_passed', False))
    print(f"  Summary: Syntax {syn_count}/{REPETITIONS}, Semantic {sem_count}/{REPETITIONS}\n")

print("="*70)
print("EXPERIMENT COMPLETE")
print("="*70)
print(f"Results: {output_file}")

matrix = {}
for game in GAMES:
    matrix[game] = {}
    matrix[game]['gemini'] = {
        'syntax': sum(1 for r in results[game]['gemini'] if r.get('syntax_passed', False)),
        'semantic': sum(1 for r in results[game]['gemini'] if r.get('semantic_passed', False))
    }

with open("results_matrix.json", 'w') as f:
    json.dump(matrix, f, indent=2)

print("Matrix: results_matrix.json")
print("\nFinal Summary:")
for game, data in matrix.items():
    print(f"  {game}: Syntax={data['gemini']['syntax']}/{REPETITIONS}, Semantic={data['gemini']['semantic']}/{REPETITIONS}")

