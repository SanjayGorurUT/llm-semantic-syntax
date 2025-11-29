import json
import os
import sys
import subprocess
import time
from testing.evaluator import evaluate_code, generate_summary
from prompts.templates import get_prompt, GAME_PROMPTS

GAMES = list(GAME_PROMPTS.keys())
REPETITIONS = 20
TEMPERATURE = 0.75
RUNTIME_ITERATIONS = 50

def call_llm_api(prompt, model_name, temperature=TEMPERATURE):
    if model_name == "openai":
        try:
            import openai
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
    elif model_name == "anthropic":
        try:
            import anthropic
            client = anthropic.Anthropic()
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4096,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return None
    elif model_name.startswith("local_"):
        try:
            model_path = model_name.replace("local_", "")
            result = subprocess.run(
                ["python", "-c", f"import sys; sys.path.insert(0, '.'); from local_llm import generate; print(generate('''{prompt}''', '{model_path}', {temperature}))"],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception as e:
            print(f"Local model error: {e}")
            return None
    else:
        print(f"Unknown model: {model_name}")
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

def run_experiment(game_name, model_name, repetition):
    prompt = get_prompt(game_name)
    print(f"  Rep {repetition+1}/{REPETITIONS}: Generating code...")
    
    response = call_llm_api(prompt, model_name, TEMPERATURE)
    if response is None:
        return None
    
    code = extract_code_from_response(response)
    if not code:
        return None
    
    print(f"  Rep {repetition+1}/{REPETITIONS}: Evaluating...")
    results = evaluate_code(code, game_name, RUNTIME_ITERATIONS)
    summary = generate_summary(results)
    
    return {
        'code': code,
        'results': results,
        'summary': summary
    }

def main():
    models = []
    if len(sys.argv) > 1:
        models = sys.argv[1].split(',')
    else:
        print("Usage: python gather_results.py <model1,model2,...>")
        print("Example: python gather_results.py openai,anthropic")
        return
    
    all_results = {}
    
    for game in GAMES:
        print(f"\n{'='*60}")
        print(f"Game: {game}")
        print(f"{'='*60}")
        all_results[game] = {}
        
        for model in models:
            print(f"\nModel: {model}")
            all_results[game][model] = []
            
            for rep in range(REPETITIONS):
                result = run_experiment(game, model, rep)
                if result:
                    all_results[game][model].append(result)
                else:
                    all_results[game][model].append({
                        'code': None,
                        'results': None,
                        'summary': {'syntax_passed': False, 'runtime_passed': False, 'semantic_passed': False, 'overall_passed': False}
                    })
                
                time.sleep(1)
            
            passed_counts = {'syntax': 0, 'runtime': 0, 'semantic': 0, 'overall': 0}
            for r in all_results[game][model]:
                if r and r.get('summary'):
                    s = r['summary']
                    if s.get('syntax_passed'):
                        passed_counts['syntax'] += 1
                    if s.get('runtime_passed'):
                        passed_counts['runtime'] += 1
                    if s.get('semantic_passed'):
                        passed_counts['semantic'] += 1
                    if s.get('overall_passed'):
                        passed_counts['overall'] += 1
            
            print(f"\n  Results for {model}:")
            print(f"    Syntax: {passed_counts['syntax']}/{REPETITIONS}")
            print(f"    Runtime: {passed_counts['runtime']}/{REPETITIONS}")
            print(f"    Semantic: {passed_counts['semantic']}/{REPETITIONS}")
            print(f"    Overall: {passed_counts['overall']}/{REPETITIONS}")
    
    output_file = f"experiment_results_{int(time.time())}.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n\nAll results saved to {output_file}")
    
    matrix = {}
    for game in GAMES:
        matrix[game] = {}
        for model in models:
            matrix[game][model] = {
                'syntax': 0,
                'runtime': 0,
                'semantic': 0
            }
            if game in all_results and model in all_results[game]:
                for r in all_results[game][model]:
                    if r and r.get('summary'):
                        s = r['summary']
                        if s.get('syntax_passed'):
                            matrix[game][model]['syntax'] += 1
                        if s.get('runtime_passed'):
                            matrix[game][model]['runtime'] += 1
                        if s.get('semantic_passed'):
                            matrix[game][model]['semantic'] += 1
    
    matrix_file = "results_matrix.json"
    with open(matrix_file, 'w') as f:
        json.dump(matrix, f, indent=2)
    print(f"Results matrix saved to {matrix_file}")

if __name__ == '__main__':
    main()

