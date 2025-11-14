import pytest
from testing.runtime_checker import check_runtime_errors

def test_runtime_valid_code():
    code = "print('Hello')\nresult = 1 + 1"
    passed, error, errors = check_runtime_errors(code, iterations=5)
    assert passed is True
    assert error is None

def test_runtime_error_code():
    code = "x = 1 / 0\nprint(x)"
    passed, error, errors = check_runtime_errors(code, iterations=5)
    assert passed is False
    assert error is not None

def test_runtime_import_error():
    code = "import nonexistent_module\nx = 5"
    passed, error, errors = check_runtime_errors(code, iterations=5)
    assert passed is False

