import json
import os
import sys
import time
from testing.evaluator import evaluate_code, generate_summary
from prompts.templates import get_prompt, GAME_PROMPTS

# API key should be set via environment variable: export GEMINI_API_KEY="your-key-here"

GAMES = ['tic_tac_toe', 'connect_four']
REPETITIONS = 3
TEMPERATURE = 0.75
RUNTIME_ITERATIONS = 5

def call_gemini_api(prompt, temperature=TEMPERATURE):
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-2.0-flash')
        print("  Calling Gemini API...", flush=True)
        response = model.generate_content(
            prompt,
            generation_config={'temperature': temperature}
        )
        return response.text
    except Exception as e:
        print(f"  Gemini API error: {e}", flush=True)
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
    print(f"  Saved to {filename}", flush=True)

def main():
    output_file = f"experiment_results_{int(time.time())}.json"
    all_results = {}
    
    print("="*60)
    print("RUNNING EXPERIMENTS SYNCHRONOUSLY")
    print("="*60)
    print(f"Games: {GAMES}")
    print(f"Repetitions per game: {REPETITIONS}")
    print(f"Results file: {output_file}")
    print("="*60)
    print()
    
    for game_idx, game in enumerate(GAMES, 1):
        print(f"\n[{game_idx}/{len(GAMES)}] Game: {game}")
        print("-" * 60)
        all_results[game] = {}
        all_results[game]['gemini'] = []
        
        prompt = get_prompt(game)
        print(f"Prompt length: {len(prompt)} characters")
        
        for rep in range(REPETITIONS):
            print(f"\n  Repetition {rep+1}/{REPETITIONS}")
            
            print("  Step 1: Generating code...")
            response = call_gemini_api(prompt, TEMPERATURE)
            if response is None:
                print("  FAILED: API call returned None")
                all_results[game]['gemini'].append({
                    'code': None,
                    'results': None,
                    'summary': {'syntax_passed': False, 'runtime_passed': False, 'semantic_passed': False, 'overall_passed': False},
                    'error': 'API call failed'
                })
                save_results(all_results, output_file)
                continue
            
            print(f"  Step 2: Extracting code (response length: {len(response)})...")
            code = extract_code_from_response(response)
            if not code or len(code) < 50:
                print(f"  FAILED: Code extraction failed or code too short ({len(code) if code else 0} chars)")
                all_results[game]['gemini'].append({
                    'code': code,
                    'results': None,
                    'summary': {'syntax_passed': False, 'runtime_passed': False, 'semantic_passed': False, 'overall_passed': False},
                    'error': 'Code extraction failed'
                })
                save_results(all_results, output_file)
                continue
            
            print(f"  Step 3: Evaluating code ({len(code)} chars)...")
            try:
                results = evaluate_code(code, game, RUNTIME_ITERATIONS)
                summary = generate_summary(results)
                
                print(f"  Results: Syntax={summary['syntax_passed']}, Runtime={summary['runtime_passed']}, Semantic={summary['semantic_passed']}")
                
                all_results[game]['gemini'].append({
                    'code': code[:500],
                    'results': results,
                    'summary': summary
                })
            except Exception as e:
                print(f"  FAILED: Evaluation error: {e}")
                all_results[game]['gemini'].append({
                    'code': code[:500],
                    'results': None,
                    'summary': {'syntax_passed': False, 'runtime_passed': False, 'semantic_passed': False, 'overall_passed': False},
                    'error': str(e)
                })
            
            save_results(all_results, output_file)
            print(f"  Progress saved. Waiting 2 seconds...")
            time.sleep(2)
        
        syntax_count = sum(1 for r in all_results[game]['gemini'] if r.get('summary', {}).get('syntax_passed', False))
        runtime_count = sum(1 for r in all_results[game]['gemini'] if r.get('summary', {}).get('runtime_passed', False))
        semantic_count = sum(1 for r in all_results[game]['gemini'] if r.get('summary', {}).get('semantic_passed', False))
        
        print(f"\n  Summary for {game}:")
        print(f"    Syntax: {syntax_count}/{REPETITIONS}")
        print(f"    Runtime: {runtime_count}/{REPETITIONS}")
        print(f"    Semantic: {semantic_count}/{REPETITIONS}")
    
    print("\n" + "="*60)
    print("EXPERIMENT COMPLETE")
    print("="*60)
    print(f"Results saved to: {output_file}")
    
    matrix = {}
    for game in GAMES:
        matrix[game] = {}
        matrix[game]['gemini'] = {
            'syntax': sum(1 for r in all_results[game]['gemini'] if r.get('summary', {}).get('syntax_passed', False)),
            'runtime': sum(1 for r in all_results[game]['gemini'] if r.get('summary', {}).get('runtime_passed', False)),
            'semantic': sum(1 for r in all_results[game]['gemini'] if r.get('summary', {}).get('semantic_passed', False))
        }
    
    matrix_file = "results_matrix.json"
    with open(matrix_file, 'w') as f:
        json.dump(matrix, f, indent=2)
    print(f"Matrix saved to: {matrix_file}")

if __name__ == '__main__':
    main()

