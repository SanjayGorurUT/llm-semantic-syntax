#!/usr/bin/env python3
"""
Consolidate results from experiment_results_full JSON files.
Combines syntax and semantic results for Gemini models.
"""

import json
import glob
import os
import sys

def load_results_file(filename):
    """Load results from a JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def consolidate_results(results_data):
    """
    Consolidate syntax and semantic results for each game and model.
    Returns a consolidated structure with counts and percentages.
    """
    consolidated = {}
    
    for game_name, game_data in results_data.items():
        consolidated[game_name] = {}
        
        for model_name, model_results in game_data.items():
            if not isinstance(model_results, list):
                continue
            
            total = len(model_results)
            syntax_passed = sum(1 for r in model_results if r.get('syntax_passed', False))
            semantic_passed = sum(1 for r in model_results if r.get('semantic_passed', False))
            game_logic_passed = sum(1 for r in model_results if r.get('game_logic_passed', False))
            
            consolidated[game_name][model_name] = {
                'total': total,
                'syntax': {
                    'passed': syntax_passed,
                    'failed': total - syntax_passed,
                    'percentage': round(syntax_passed / total * 100, 1) if total > 0 else 0
                },
                'semantic': {
                    'passed': semantic_passed,
                    'failed': total - semantic_passed,
                    'percentage': round(semantic_passed / total * 100, 1) if total > 0 else 0
                },
                'game_logic': {
                    'passed': game_logic_passed,
                    'failed': total - game_logic_passed,
                    'percentage': round(game_logic_passed / total * 100, 1) if total > 0 else 0
                } if any('game_logic_passed' in r for r in model_results) else None
            }
    
    return consolidated

def create_summary_matrix(results_data):
    """
    Create a simple matrix format for easy viewing.
    Format: {game: {model: {syntax: count, semantic: count, game_logic: count}}}
    """
    matrix = {}
    
    for game_name, game_data in results_data.items():
        matrix[game_name] = {}
        
        for model_name, model_results in game_data.items():
            if not isinstance(model_results, list):
                continue
            
            total = len(model_results)
            syntax_count = sum(1 for r in model_results if r.get('syntax_passed', False))
            semantic_count = sum(1 for r in model_results if r.get('semantic_passed', False))
            game_logic_count = sum(1 for r in model_results if r.get('game_logic_passed', False)) if any('game_logic_passed' in r for r in model_results) else None
            
            matrix[game_name][model_name] = {
                'syntax': syntax_count,
                'semantic': semantic_count
            }
            
            if game_logic_count is not None:
                matrix[game_name][model_name]['game_logic'] = game_logic_count
    
    return matrix

def main():
    # Find the latest experiment_results_full JSON file
    files = glob.glob("experiment_results_full_*.json")
    if not files:
        print("No experiment_results_full_*.json files found")
        return
    
    latest_file = max(files, key=os.path.getctime)
    print(f"Loading results from: {latest_file}")
    
    results_data = load_results_file(latest_file)
    if results_data is None:
        print("Failed to load results")
        return
    
    # Consolidate results
    consolidated = consolidate_results(results_data)
    
    # Save consolidated results
    consolidated_file = "results_consolidated.json"
    with open(consolidated_file, 'w') as f:
        json.dump(consolidated, f, indent=2)
    print(f"Consolidated results saved to: {consolidated_file}")
    
    # Create and save matrix
    matrix = create_summary_matrix(results_data)
    matrix_file = "results_matrix.json"
    with open(matrix_file, 'w') as f:
        json.dump(matrix, f, indent=2)
    print(f"Matrix saved to: {matrix_file}")
    
    # Print summary
    print("\n" + "="*70)
    print("CONSOLIDATED RESULTS SUMMARY")
    print("="*70)
    
    for game_name, game_data in consolidated.items():
        print(f"\n{game_name.upper()}:")
        for model_name, stats in game_data.items():
            print(f"  {model_name}:")
            print(f"    Syntax: {stats['syntax']['passed']}/{stats['total']} ({stats['syntax']['percentage']}%)")
            print(f"    Semantic: {stats['semantic']['passed']}/{stats['total']} ({stats['semantic']['percentage']}%)")
            if stats['game_logic']:
                print(f"    Game Logic: {stats['game_logic']['passed']}/{stats['total']} ({stats['game_logic']['percentage']}%)")
    
    print("\n" + "="*70)
    print("MATRIX FORMAT")
    print("="*70)
    for game_name, game_data in matrix.items():
        print(f"\n{game_name}:")
        for model_name, counts in game_data.items():
            print(f"  {model_name}: {counts}")

if __name__ == '__main__':
    main()

