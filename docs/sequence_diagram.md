# Sequence Diagram: Taking Out a Loan

```text
Customer       Main Menu       Banking Menu       Account        Loan Module
   |               |                |                |                |
   |--- Select 4 ->|                |                |                |
   |               |--- loan_menu()->                |                |
   |               |                |--- room_for()->|                |
   |               |                |<-- returns limit--------------|
   |               |                |                |                |
   |--- Input Type, Amount & Months----------------->|                |
   |               |                |                |--- emi_for()-->|
   |               |                |                |<-- returns emi-|
   |               |                |                |                |
   |--- Confirm (y)->               |                |                |
   |               |                |--- take_loan()->                |
   |               |                |    (Adds Loan, deducts fees/GST)|
   |               |                |<-- Success --------------------|
   |<-- Displays Approval & EMI-----|                |                |