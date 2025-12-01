import os
import json
import glob

print("Checking experiment progress...\n")

result_files = glob.glob("experiment_results_*.json")
if result_files:
    latest = max(result_files, key=os.path.getctime)
    print(f"Latest results file: {latest}\n")
    
    with open(latest, 'r') as f:
        data = json.load(f)
    
    for game_name, game_data in data.items():
        if isinstance(game_data, dict):
            print(f"{game_name}:")
            for model_name, model_data in game_data.items():
                if isinstance(model_data, list):
                    total = len(model_data)
                    completed = sum(1 for r in model_data if r and r.get('code'))
                    print(f"  {model_name}: {completed}/{total} completed")
            print()
else:
    print("No results files found yet. Experiment may still be running...")

