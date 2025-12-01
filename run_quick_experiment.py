import json
import os
import sys
import time
from testing.syntax_checker import validate_syntax
from testing.semantic_checker import check_semantic_correctness
from prompts.templates import get_prompt, GAME_PROMPTS

# API key should be set via environment variable: export GEMINI_API_KEY="your-key-here"

GAMES = ['tic_tac_toe', 'connect_four', 'snake_game', 'ball_bouncing', 'snakes_and_ladders']
REPETITIONS = 5
TEMPERATURE = 0.75

def call_gemini_api(prompt, temperature=TEMPERATURE):
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(
            prompt,
            generation_config={'temperature': temperature}
        )
        return response.text
    except Exception as e:
        print(f"  API error: {e}")
        return None

def extract_code_from_response(response):
    if "```python" in response:
        start = response.find("```python") + 9
        end = response.find("```", start)
        return response[start:end].strip()
    elif "```" in response:
        start = response.find("```") + 3
        end = response.find("```", start)
        return response[start:end].strip()
    return response.strip()

def save_results(all_results, filename):
    with open(filename, 'w') as f:
        json.dump(all_results, f, indent=2)

def main():
    output_file = f"experiment_results_{int(time.time())}.json"
    all_results = {}
    
    print("="*70)
    print("QUICK EXPERIMENT - Syntax & Semantic Only (No Runtime)")
    print("="*70)
    print(f"Games: {len(GAMES)}")
    print(f"Repetitions: {REPETITIONS}")
    print(f"Output: {output_file}")
    print("="*70)
    print()
    
    for game_idx, game in enumerate(GAMES, 1):
        print(f"\n[{game_idx}/{len(GAMES)}] {game}")
        print("-" * 70)
        all_results[game] = {}
        all_results[game]['gemini'] = []
        
        prompt = get_prompt(game)
        
        for rep in range(REPETITIONS):
            print(f"  Rep {rep+1}/{REPETITIONS}: ", end="", flush=True)
            
            response = call_gemini_api(prompt, TEMPERATURE)
            if response is None:
                print("API FAILED")
                all_results[game]['gemini'].append({
                    'code': None,
                    'syntax_passed': False,
                    'semantic_passed': False,
                    'error': 'API call failed'
                })
                save_results(all_results, output_file)
                continue
            
            code = extract_code_from_response(response)
            if not code or len(code) < 50:
                print("EXTRACTION FAILED")
                all_results[game]['gemini'].append({
                    'code': code[:200] if code else None,
                    'syntax_passed': False,
                    'semantic_passed': False,
                    'error': 'Code extraction failed'
                })
                save_results(all_results, output_file)
                continue
            
            print(f"Code generated ({len(code)} chars), checking... ", end="", flush=True)
            
            syntax_ok, error_type, error_msg = validate_syntax(code)
            semantic_ok, semantic_error = check_semantic_correctness(code, game)
            
            result = {
                'code_length': len(code),
                'syntax_passed': syntax_ok,
                'semantic_passed': semantic_ok,
                'syntax_error': error_msg if not syntax_ok else None,
                'semantic_error': semantic_error if not semantic_ok else None
            }
            
            all_results[game]['gemini'].append(result)
            save_results(all_results, output_file)
            
            syn_str = "✓" if syntax_ok else "✗"
            sem_str = "✓" if semantic_ok else "✗"
            print(f"Syntax:{syn_str} Semantic:{sem_str}")
            
            time.sleep(1)
        
        syn_count = sum(1 for r in all_results[game]['gemini'] if r.get('syntax_passed', False))
        sem_count = sum(1 for r in all_results[game]['gemini'] if r.get('semantic_passed', False))
        print(f"  Summary: Syntax {syn_count}/{REPETITIONS}, Semantic {sem_count}/{REPETITIONS}")
    
    print("\n" + "="*70)
    print("EXPERIMENT COMPLETE")
    print("="*70)
    print(f"Results: {output_file}")
    
    matrix = {}
    for game in GAMES:
        matrix[game] = {}
        matrix[game]['gemini'] = {
            'syntax': sum(1 for r in all_results[game]['gemini'] if r.get('syntax_passed', False)),
            'semantic': sum(1 for r in all_results[game]['gemini'] if r.get('semantic_passed', False))
        }
    
    with open("results_matrix.json", 'w') as f:
        json.dump(matrix, f, indent=2)
    
    print("\nSummary Matrix:")
    for game, data in matrix.items():
        print(f"  {game}: Syntax={data['gemini']['syntax']}/{REPETITIONS}, Semantic={data['gemini']['semantic']}/{REPETITIONS}")

if __name__ == '__main__':
    main()

