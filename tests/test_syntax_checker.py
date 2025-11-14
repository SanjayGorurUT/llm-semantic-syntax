import pytest
from testing.syntax_checker import check_syntax, validate_syntax

def test_valid_syntax():
    code = "x = 1 + 2\nprint(x)"
    result, error = check_syntax(code)
    assert result is True
    assert error is None

def test_invalid_syntax():
    code = "x = 1 +\nprint(x"
    result, error = check_syntax(code)
    assert result is False
    assert error is not None

def test_validate_syntax_valid():
    code = "import pygame\nx = 5"
    valid, error_type, error_msg = validate_syntax(code)
    assert valid is True

def test_validate_syntax_invalid():
    code = "x = 1 +\ndef"
    valid, error_type, error_msg = validate_syntax(code)
    assert valid is False
    assert error_type is not None

