import json
import os
import sys

def load_results(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def calculate_stats(results_data):
    stats = {}
    
    for game_name, game_data in results_data.items():
        if not isinstance(game_data, dict):
            continue
        
        stats[game_name] = {}
        
        for model_name, model_data in game_data.items():
            if not isinstance(model_data, list):
                continue
            
            total = len(model_data)
            if total == 0:
                continue
            
            syntax_pass = sum(1 for r in model_data if r and r.get('summary', {}).get('syntax_passed', False))
            runtime_pass = sum(1 for r in model_data if r and r.get('summary', {}).get('runtime_passed', False))
            semantic_pass = sum(1 for r in model_data if r and r.get('summary', {}).get('semantic_passed', False))
            overall_pass = sum(1 for r in model_data if r and r.get('summary', {}).get('overall_passed', False))
            
            stats[game_name][model_name] = {
                'total': total,
                'syntax_rate': syntax_pass / total,
                'runtime_rate': runtime_pass / total,
                'semantic_rate': semantic_pass / total,
                'overall_rate': overall_pass / total,
                'syntax_count': syntax_pass,
                'runtime_count': runtime_pass,
                'semantic_count': semantic_pass,
                'overall_count': overall_pass
            }
    
    return stats

def print_summary(stats):
    print("\n" + "="*80)
    print("RESULTS SUMMARY")
    print("="*80)
    
    for game_name, game_stats in stats.items():
        print(f"\n{game_name.upper()}")
        print("-" * 80)
        
        for model_name, model_stats in game_stats.items():
            print(f"\n  Model: {model_name}")
            print(f"    Syntax:     {model_stats['syntax_count']}/{model_stats['total']} ({model_stats['syntax_rate']*100:.1f}%)")
            print(f"    Runtime:    {model_stats['runtime_count']}/{model_stats['total']} ({model_stats['runtime_rate']*100:.1f}%)")
            print(f"    Semantic:   {model_stats['semantic_count']}/{model_stats['total']} ({model_stats['semantic_rate']*100:.1f}%)")
            print(f"    Overall:    {model_stats['overall_count']}/{model_stats['total']} ({model_stats['overall_rate']*100:.1f}%)")

def create_matrix(results_data):
    matrix = {}
    
    for game_name, game_data in results_data.items():
        if not isinstance(game_data, dict):
            continue
        
        matrix[game_name] = {}
        
        for model_name, model_data in game_data.items():
            if not isinstance(model_data, list):
                continue
            
            syntax_count = 0
            runtime_count = 0
            semantic_count = 0
            
            for r in model_data:
                if r and r.get('summary'):
                    s = r['summary']
                    if s.get('syntax_passed'):
                        syntax_count += 1
                    if s.get('runtime_passed'):
                        runtime_count += 1
                    if s.get('semantic_passed'):
                        semantic_count += 1
            
            matrix[game_name][model_name] = {
                'syntax': syntax_count,
                'runtime': runtime_count,
                'semantic': semantic_count
            }
    
    return matrix

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_results.py <results_file.json>")
        return
    
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return
    
    results = load_results(filename)
    stats = calculate_stats(results)
    print_summary(stats)
    
    matrix = create_matrix(results)
    matrix_file = filename.replace('.json', '_matrix.json')
    with open(matrix_file, 'w') as f:
        json.dump(matrix, f, indent=2)
    print(f"\nMatrix saved to {matrix_file}")
    
    stats_file = filename.replace('.json', '_stats.json')
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"Statistics saved to {stats_file}")

if __name__ == '__main__':
    main()

