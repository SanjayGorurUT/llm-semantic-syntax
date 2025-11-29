import json
import os
import sys
from testing.evaluator import evaluate_code, generate_summary
from prompts.templates import get_prompt, GAME_PROMPTS

GAMES = list(GAME_PROMPTS.keys())

def load_code_from_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading file {filepath}: {e}")
        return None

def save_results(data, filename='results.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def eval_game(game_name, code_str, iters=50):
    results = evaluate_code(code_str, game_name, iters)
    summary = generate_summary(results)
    return results, summary

def main():
    if len(sys.argv) > 1:
        code_dir = sys.argv[1]
    else:
        code_dir = None
    
    results_data = {}
    
    for game in GAMES:
        print(f"\nProcessing {game}...")
        
        if code_dir:
            code_file = os.path.join(code_dir, f"{game}.py")
            if not os.path.exists(code_file):
                print(f"  Code file not found: {code_file}")
                continue
            code = load_code_from_file(code_file)
            if code is None:
                continue
        else:
            code_file = f"games/{game}.py"
            if not os.path.exists(code_file):
                print(f"  Reference file not found: {code_file}")
                continue
            code = load_code_from_file(code_file)
            if code is None:
                continue
        
        res, summ = eval_game(game, code, 10)
        
        results_data[game] = {
            'syntax': summ['syntax_passed'],
            'runtime': summ['runtime_passed'],
            'semantic': summ['semantic_passed'],
            'overall': summ['overall_passed'],
            'details': res
        }
        
        print(f"  Syntax: {'PASS' if summ['syntax_passed'] else 'FAIL'}")
        print(f"  Runtime: {'PASS' if summ['runtime_passed'] else 'FAIL'}")
        print(f"  Semantic: {'PASS' if summ['semantic_passed'] else 'FAIL'}")
    
    save_results(results_data)
    print("\nResults written to results.json")
    return results_data

if __name__ == '__main__':
    main()

