# Application Workflow

1. **Initialization**: 
   - User launches application via `python -m src.main`.
   - Welcome banner displays, and the user enters their name and an initial opening deposit (minimum Rs.10,000 required).
2. **Main Dashboard Loop**:
   - Displays real-time account balance and outstanding loans.
   - Presents an 8-option interactive menu:
     1. Deposit Funds
     2. Withdraw Funds (generates slip)
     3. Check Balance & Net Worth
     4. Apply for Loans (Home, Personal, Business, Education)
     5. My Loans & Repayments
     6. Fast-Forward Time (compounds savings interest & deducts tax)
     7. View Transaction History
     8. Exit & Export Itemized Statement
3. **Termination**:
   - Saves statement file to `bills here/` and gracefully terminates.