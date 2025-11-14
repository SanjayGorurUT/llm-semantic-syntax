import pytest
from testing.evaluator import evaluate_code, generate_summary

def test_evaluate_valid_code():
    code = "print('test')"
    results = evaluate_code(code, 'tic_tac_toe', runtime_iterations=5)
    assert 'syntax' in results
    assert 'runtime' in results
    assert 'semantic' in results

def test_evaluate_invalid_syntax():
    code = "x = 1 +"
    results = evaluate_code(code, 'tic_tac_toe', runtime_iterations=5)
    assert results['syntax']['passed'] is False

def test_generate_summary():
    results = {
        'syntax': {'passed': True, 'error': None},
        'runtime': {'passed': True, 'error': None, 'errors': []},
        'semantic': {'passed': True, 'error': None}
    }
    summary = generate_summary(results)
    assert summary['syntax_passed'] is True
    assert summary['runtime_passed'] is True
    assert summary['semantic_passed'] is True
    assert summary['overall_passed'] is True

