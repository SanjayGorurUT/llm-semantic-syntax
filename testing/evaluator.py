from .syntax_checker import validate_syntax
from .runtime_checker import check_runtime_errors
from .semantic_checker import check_semantic_correctness

def evaluate_code(code_string, game_name, runtime_iterations=50):
    results = {
        'syntax': {'passed': False, 'error': None},
        'runtime': {'passed': False, 'error': None, 'errors': []},
        'semantic': {'passed': False, 'error': None}
    }
    
    syntax_ok, error_type, error_msg = validate_syntax(code_string)
    results['syntax']['passed'] = syntax_ok
    results['syntax']['error'] = error_msg
    
    if not syntax_ok:
        return results
    
    runtime_ok, runtime_error, runtime_errors = check_runtime_errors(code_string, runtime_iterations)
    results['runtime']['passed'] = runtime_ok
    results['runtime']['error'] = runtime_error
    results['runtime']['errors'] = runtime_errors
    
    semantic_ok, semantic_error = check_semantic_correctness(code_string, game_name)
    results['semantic']['passed'] = semantic_ok
    results['semantic']['error'] = semantic_error
    
    return results

def generate_summary(results):
    summary = {
        'syntax_passed': results['syntax']['passed'],
        'runtime_passed': results['runtime']['passed'],
        'semantic_passed': results['semantic']['passed'],
        'overall_passed': results['syntax']['passed'] and results['runtime']['passed'] and results['semantic']['passed']
    }
    return summary

