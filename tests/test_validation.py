import pytest
from unittest.mock import patch
from src.validation import get_amount

def test_get_amount_valid():
    with patch('builtins.input', return_value='5000'):
        result = get_amount()
        assert result == 5000.0

def test_get_amount_invalid():
    with patch('builtins.input', return_value='abc'):
        result = get_amount()
        assert result == 0.0