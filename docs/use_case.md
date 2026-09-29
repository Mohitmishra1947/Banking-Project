# Use Case Specifications

## UC-01: Open Account
- **Actor**: Customer
- **Description**: User inputs name and initial opening deposit. System verifies deposit meets minimum threshold (Rs.10,000).

## UC-02: Manage Loans
- **Actor**: Customer
- **Description**: User selects a loan category. System calculates borrowing limit based on balance multipliers, applies processing fees and GST, and sets up monthly EMIs.

## UC-03: Simulate Time
- **Actor**: Customer
- **Description**: User advances time by a specified number of months. System computes monthly savings interest, applies 10% TDS tax, and accumulates loan interest.

## UC-04: Generate Statement
- **Actor**: Customer / System
- **Description**: User exits app or requests statement. System outputs an itemized breakdown of transactions, balances, and remaining liabilities to a saved text report.