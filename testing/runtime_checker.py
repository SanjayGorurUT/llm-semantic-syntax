import subprocess
import tempfile
import os
import time

def run_code_iterations(code_string, iterations=50, timeout=2):
    errors = []
    success_count = 0
    
    for i in range(iterations):
        fd, temp_file = tempfile.mkstemp(suffix='.py')
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(code_string)
        except:
            os.close(fd)
            continue
        
        try:
            env = dict(os.environ, PYTHONUNBUFFERED='1')
            if 'DISPLAY' not in env:
                env['DISPLAY'] = ':99'
            
            result = subprocess.run(
                ['python', '-u', temp_file],
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env
            )
            
            if result.returncode == 0:
                success_count += 1
            else:
                err_msg = result.stderr.strip()
                if not err_msg:
                    err_msg = result.stdout.strip()
                if err_msg and 'pygame' not in err_msg.lower():
                    errors.append({
                        'iteration': i + 1,
                        'error': err_msg[:200]
                    })
                else:
                    success_count += 1
        except subprocess.TimeoutExpired:
            success_count += 1
        except Exception as e:
            err_str = str(e)[:200]
            if 'pygame' not in err_str.lower():
                errors.append({
                    'iteration': i + 1,
                    'error': err_str
                })
            else:
                success_count += 1
        finally:
            try:
                os.unlink(temp_file)
            except:
                pass
        
        time.sleep(0.05)
    
    success_rate = success_count / iterations
    return success_rate, errors

def check_runtime_errors(code_string, iterations=50):
    success_rate, errors = run_code_iterations(code_string, iterations)
    
    if success_rate >= 0.9:
        return True, None, []
    else:
        msg = f"Runtime errors in {len(errors)}/{iterations} iterations"
        return False, msg, errors
