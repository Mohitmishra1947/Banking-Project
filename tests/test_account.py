import pytest
from src.account import Account

def test_account_creation():
    acc = Account("Test User", 15000)
    assert acc.name == "Test User"
    assert acc.balance == 15000
    assert acc.opening == 15000
    assert acc.loan == 0

def test_deposit():
    acc = Account("Test User", 10000)
    acc.deposit(5000)
    assert acc.balance == 15000
    assert acc.deposited == 5000

def test_deposit_invalid():
    acc = Account("Test User", 10000)
    acc.deposit(-500)
    assert acc.balance == 10000  # Balance shouldn't change

def test_withdraw_success():
    acc = Account("Test User", 20000)
    acc.withdraw(5000)
    assert acc.balance == 15000
    assert acc.withdrawn == 5000

def test_withdraw_insufficient():
    acc = Account("Test User", 10000)
    acc.withdraw(15000)
    assert acc.balance == 10000  # Unchanged