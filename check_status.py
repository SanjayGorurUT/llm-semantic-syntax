import os
import subprocess
import json
import glob
import time
from datetime import datetime

def check_process():
    result = subprocess.run(
        ['ps', 'aux'],
        capture_output=True,
        text=True
    )
    processes = [p for p in result.stdout.split('\n') if 'gather_results' in p and 'grep' not in p]
    return len(processes) > 0, processes

def check_results_files():
    files = glob.glob("experiment_results_*.json")
    if files:
        latest = max(files, key=os.path.getctime)
        mtime = os.path.getmtime(latest)
        age = time.time() - mtime
        return latest, age, True
    return None, 0, False

def analyze_progress():
    files = glob.glob("experiment_results_*.json")
    if not files:
        return None
    
    latest = max(files, key=os.path.getctime)
    try:
        with open(latest, 'r') as f:
            data = json.load(f)
        
        total_games = 5
        total_reps = 20
        
        progress = {}
        for game_name, game_data in data.items():
            if isinstance(game_data, dict):
                for model_name, model_data in game_data.items():
                    if isinstance(model_data, list):
                        completed = sum(1 for r in model_data if r and r.get('code'))
                        progress[f"{game_name}_{model_name}"] = {
                            'completed': completed,
                            'total': len(model_data),
                            'percentage': (completed / len(model_data) * 100) if len(model_data) > 0 else 0
                        }
        
        return progress, latest
    except:
        return None, latest

print("=" * 60)
print("EXPERIMENT STATUS CHECKER")
print("=" * 60)
print()

is_running, processes = check_process()

if is_running:
    print("✓ Process is RUNNING")
    print(f"  Found {len(processes)} process(es)")
    print()
else:
    print("✗ Process is NOT RUNNING")
    print()

result_file, age, exists = check_results_files()

if exists:
    print(f"✓ Results file found: {result_file}")
    print(f"  Last updated: {int(age)} seconds ago")
    print()
    
    progress, latest = analyze_progress()
    if progress:
        print("Progress Summary:")
        print("-" * 60)
        total_completed = 0
        total_expected = 0
        
        for key, stats in progress.items():
            game, model = key.rsplit('_', 1)
            print(f"  {game} ({model}): {stats['completed']}/{stats['total']} ({stats['percentage']:.1f}%)")
            total_completed += stats['completed']
            total_expected += stats['total']
        
        print("-" * 60)
        overall_pct = (total_completed / total_expected * 100) if total_expected > 0 else 0
        print(f"  Overall: {total_completed}/{total_expected} ({overall_pct:.1f}%)")
        print()
        
        if is_running:
            remaining = total_expected - total_completed
            if remaining > 0:
                print(f"  Estimated remaining: ~{remaining} API calls")
                print(f"  (Each call takes ~10-30 seconds)")
        else:
            print("  ✓ Experiment appears to be COMPLETE!")
            print(f"  Run: python analyze_results.py {latest}")
    else:
        print("  (File exists but couldn't parse progress)")
else:
    print("✗ No results file found yet")
    if is_running:
        print("  (Experiment just started, results will appear soon)")

print()
print("=" * 60)
print(f"Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

