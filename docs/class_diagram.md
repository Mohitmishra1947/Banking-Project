# Class Diagram Overview

```text
+-----------------------------------+
|              Account              |
+-----------------------------------+
| + name: str                       |
| + balance: float                  |
| + loans: List[Loan]               |
| + months: int                     |
| + history: List[tuple]            |
+-----------------------------------+
| + deposit(amount)                 |
| + withdraw(amount)                |
| + check_balance()                 |
| + room_for(kind)                  |
| + take_loan(kind, amount, months) |
| + repay_loan(loan, amount)        |
| + fast_forward(months)            |
| + show_history()                  |
| + print_bill()                    |
+-----------------------------------+
                   |
                   | contains 0..*
                   v
+-----------------------------------+
|               Loan                |
+-----------------------------------+
| + kind: dict                      |
| + name: str                       |
| + rate: float                     |
| + principal: float                |
| + outstanding: float              |
| + months: int                     |
| + emi: float                      |
+-----------------------------------+