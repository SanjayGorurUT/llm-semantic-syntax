import json
import os
import ast
import time

os.environ['GEMINI_API_KEY'] = "AIzaSyD_1pSTy7EohE7zMz_qEGoYlCl4V2buZFQ"

GAMES = ['tic_tac_toe', 'connect_four']
REPETITIONS = 3
TEMPERATURE = 0.75

def call_gemini(prompt):
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt, generation_config={'temperature': TEMPERATURE})
        return response.text
    except Exception as e:
        return f"ERROR: {str(e)}"

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

def check_syntax_only(code):
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Parse error: {str(e)}"

prompts = {
    'tic_tac_toe': "Create a Python pygame game for Tic-Tac-Toe. Write complete runnable code with a 3x3 grid, two players, win detection, and restart functionality.",
    'connect_four': "Create a Python pygame game for Connect Four. Write complete runnable code with a 6x7 board, piece dropping, and win detection."
}

results = {}

print("Starting minimal experiment...")
print(f"Games: {GAMES}")
print(f"Repetitions: {REPETITIONS}\n")

for game in GAMES:
    print(f"Game: {game}")
    results[game] = {'gemini': []}
    
    prompt = prompts[game]
    
    for rep in range(REPETITIONS):
        print(f"  Rep {rep+1}/{REPETITIONS}... ", end="", flush=True)
        
        response = call_gemini(prompt)
        if response.startswith("ERROR"):
            print(f"API FAILED: {response}")
            results[game]['gemini'].append({'syntax': False, 'error': response})
            continue
        
        code = extract_code(response)
        if len(code) < 100:
            print(f"CODE TOO SHORT ({len(code)} chars)")
            results[game]['gemini'].append({'syntax': False, 'error': 'Code too short'})
            continue
        
        syntax_ok, syntax_err = check_syntax_only(code)
        print(f"Syntax: {'PASS' if syntax_ok else 'FAIL'}")
        
        results[game]['gemini'].append({
            'syntax_passed': syntax_ok,
            'code_length': len(code),
            'syntax_error': syntax_err if not syntax_ok else None
        })
        
        time.sleep(2)
    
    syn_pass = sum(1 for r in results[game]['gemini'] if r.get('syntax_passed', False))
    print(f"  Summary: {syn_pass}/{REPETITIONS} passed syntax\n")

output_file = f"results_minimal_{int(time.time())}.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to: {output_file}")

matrix = {}
for game in GAMES:
    matrix[game] = {}
    matrix[game]['gemini'] = {
        'syntax': sum(1 for r in results[game]['gemini'] if r.get('syntax_passed', False))
    }

with open("results_matrix.json", 'w') as f:
    json.dump(matrix, f, indent=2)

print("Matrix saved to: results_matrix.json")
print("\nDone!")

