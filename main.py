import json
import os
from testing.evaluator import evaluate_code, generate_summary
from prompts.templates import get_prompt, GAME_PROMPTS

GAMES = list(GAME_PROMPTS.keys())

def load_llm_code(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def save_results(results, output_file='results.json'):
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

def run_evaluation(game_name, code_string, iterations=50):
    print(f"Evaluating {game_name}...")
    results = evaluate_code(code_string, game_name, iterations)
    summary = generate_summary(results)
    return results, summary

def main():
    results_matrix = {}
    
    for game_name in GAMES:
        prompt = get_prompt(game_name)
        print(f"\nGame: {game_name}")
        print(f"Prompt length: {len(prompt)} characters")
        
        reference_file = f"games/{game_name}.py"
        if os.path.exists(reference_file):
            with open(reference_file, 'r') as f:
                reference_code = f.read()
            
            results, summary = run_evaluation(game_name, reference_code, iterations=10)
            
            results_matrix[game_name] = {
                'syntax': summary['syntax_passed'],
                'runtime': summary['runtime_passed'],
                'semantic': summary['semantic_passed'],
                'overall': summary['overall_passed'],
                'details': results
            }
            
            print(f"  Syntax: {'PASS' if summary['syntax_passed'] else 'FAIL'}")
            print(f"  Runtime: {'PASS' if summary['runtime_passed'] else 'FAIL'}")
            print(f"  Semantic: {'PASS' if summary['semantic_passed'] else 'FAIL'}")
        else:
            print(f"  Reference file not found: {reference_file}")
    
    save_results(results_matrix, 'results.json')
    print("\nResults saved to results.json")
    
    return results_matrix

if __name__ == '__main__':
    main()

