import subprocess
import tempfile
import os
import signal
import time

def run_code_iterations(code_string, iterations=50, timeout=5):
    errors = []
    success_count = 0
    
    for i in range(iterations):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code_string)
            temp_file = f.name
        
        try:
            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=timeout,
                env={**os.environ, 'PYTHONUNBUFFERED': '1'}
            )
            
            if result.returncode == 0:
                success_count += 1
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                if error_msg:
                    errors.append({
                        'iteration': i + 1,
                        'error': error_msg[:200]
                    })
        except subprocess.TimeoutExpired:
            errors.append({
                'iteration': i + 1,
                'error': 'Timeout'
            })
        except Exception as e:
            errors.append({
                'iteration': i + 1,
                'error': str(e)[:200]
            })
        finally:
            try:
                os.unlink(temp_file)
            except:
                pass
        
        time.sleep(0.1)
    
    success_rate = success_count / iterations
    return success_rate, errors

def check_runtime_errors(code_string, iterations=50):
    success_rate, errors = run_code_iterations(code_string, iterations)
    
    if success_rate == 1.0:
        return True, None, []
    else:
        return False, f"Runtime errors in {len(errors)}/{iterations} iterations", errors

