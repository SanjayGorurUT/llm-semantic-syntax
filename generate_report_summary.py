import json
import glob
import os

def load_latest_results():
    files = glob.glob("experiment_results_with_logic_*.json")
    if not files:
        files = glob.glob("experiment_results_full_*.json")
    if not files:
        return None, None
    
    latest = max(files, key=os.path.getctime)
    with open(latest, 'r') as f:
        return json.load(f), latest

def generate_summary(results_file):
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    print("="*80)
    print("EXPERIMENT RESULTS SUMMARY")
    print("="*80)
    print()
    
    total_reps = 0
    syntax_pass = 0
    semantic_pass = 0
    logic_pass = 0
    
    for game_name, game_data in data.items():
        if not isinstance(game_data, dict) or 'gemini' not in game_data:
            continue
        
        reps = game_data['gemini']
        total_reps += len(reps)
        
        game_syntax = sum(1 for r in reps if r.get('syntax_passed', False))
        game_semantic = sum(1 for r in reps if r.get('semantic_passed', False))
        game_logic = sum(1 for r in reps if r.get('game_logic_passed', False))
        
        syntax_pass += game_syntax
        semantic_pass += game_semantic
        logic_pass += game_logic
        
        print(f"{game_name.upper().replace('_', ' ')}:")
        print(f"  Syntax:     {game_syntax}/{len(reps)} ({game_syntax/len(reps)*100:.1f}%)")
        print(f"  Semantic:   {game_semantic}/{len(reps)} ({game_semantic/len(reps)*100:.1f}%)")
        if game_logic > 0 or any('game_logic_passed' in r for r in reps):
            print(f"  Game Logic: {game_logic}/{len(reps)} ({game_logic/len(reps)*100:.1f}%)")
        print()
    
    print("="*80)
    print("OVERALL STATISTICS")
    print("="*80)
    print(f"Total code generations: {total_reps}")
    print(f"Syntax accuracy:   {syntax_pass}/{total_reps} ({syntax_pass/total_reps*100:.1f}%)")
    print(f"Semantic accuracy: {semantic_pass}/{total_reps} ({semantic_pass/total_reps*100:.1f}%)")
    if logic_pass > 0:
        print(f"Game logic accuracy: {logic_pass}/{total_reps} ({logic_pass/total_reps*100:.1f}%)")
    print("="*80)
    
    matrix = {}
    for game_name, game_data in data.items():
        if not isinstance(game_data, dict) or 'gemini' not in game_data:
            continue
        reps = game_data['gemini']
        matrix[game_name] = {
            'gemini': {
                'syntax': sum(1 for r in reps if r.get('syntax_passed', False)),
                'semantic': sum(1 for r in reps if r.get('semantic_passed', False)),
                'game_logic': sum(1 for r in reps if r.get('game_logic_passed', False)) if any('game_logic_passed' in r for r in reps) else 0
            }
        }
    
    matrix_file = "final_results_matrix.json"
    with open(matrix_file, 'w') as f:
        json.dump(matrix, f, indent=2)
    print(f"\nMatrix saved to: {matrix_file}")
    
    return matrix

if __name__ == '__main__':
    data, filename = load_latest_results()
    if data:
        print(f"Loading results from: {filename}\n")
        generate_summary(filename)
    else:
        print("No results files found!")

