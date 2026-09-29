import pytest
from src.loan import Loan, LOAN_TYPES, emi_for

def test_emi_calculation():
    # Test for a simple principal, rate, and months
    principal = 100000
    annual_rate = 0.10
    months = 12
    emi = emi_for(principal, annual_rate, months)
    assert emi > 0
    assert round(emi, 2) == 8791.59

def test_loan_initialization():
    kind = LOAN_TYPES["2"]  # Personal Loan
    loan = Loan(kind, 50000, 12)
    assert loan.name == "Personal Loan"
    assert loan.principal == 50000
    assert loan.outstanding == 50000
    assert loan.months == 12
    assert loan.emi > 0