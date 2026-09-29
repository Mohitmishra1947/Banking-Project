from src.ui import section, c, rs, time_text, bad, info, banner
from src.loan import LOAN_TYPES, GST, emi_for
from src.validation import get_amount

def loan_menu(account):
    section("LOAN OFFERS", "magenta")
    print(c(f"  {'#':<3}{'Type':<17}{'Rate':<8}{'Fee':<8}{'Up to':<11}{'Max time'}", "bold"))
    for key, k in LOAN_TYPES.items():
        print(f"  {key:<3}{k['name']:<17}{k['rate'] * 100:<8.2f}"
              f"{k['fee'] * 100:<8.2f}{str(k['limit']) + 'x balance':<11}"
              f"{time_text(k['max_months'])}")
        print(c(f"     {k['icon']} {k['tag']}", "dim"))
    print("  0  Back")

    choice = input("\n  Choose loan type (0-4): ").strip()
    if choice == "0":
        return
    kind = LOAN_TYPES.get(choice)
    if not kind:
        bad("Invalid choice.")
        return

    room = account.room_for(kind)
    section(kind["name"].upper(), "magenta")
    print(f"  Interest rate : {kind['rate'] * 100:g}% per year")
    print(f"  Fee           : {kind['fee'] * 100:g}% + {GST * 100:.0f}% GST on the fee")
    print(f"  Minimum loan  : {rs(kind['min'])}")
    print(f"  You can borrow: {c(rs(room), 'green')}")

    if room < kind["min"]:
        bad(f"Your balance is too low for a {kind['name']} right now.")
        return

    amount = get_amount("  Loan amount: Rs.")
    if amount < kind["min"]:
        bad(f"Minimum for a {kind['name']} is {rs(kind['min'])}.")
        return
    if amount > room:
        bad(f"Loan limit reached. You can borrow up to {rs(room)}.")
        return

    months = get_amount(f"  Time in months (6 to {kind['max_months']}): ")
    if not 6 <= months <= kind["max_months"]:
        bad(f"Choose between 6 and {kind['max_months']} months.")
        return
    months = int(months)

    emi = emi_for(amount, kind["rate"], months)
    fee = round(amount * kind["fee"], 2)
    gst = round(fee * GST, 2)
    section("YOUR OFFER", "yellow")
    print(f"  Monthly EMI  : {c(rs(emi), 'yellow')}")
    print(f"  Total to pay : {rs(emi * months)}")
    print(f"  Fee + GST    : {rs(fee + gst)}")
    print(f"  You receive  : {rs(amount - fee - gst)}")

    if input("\n  Confirm this loan? (y/n): ").strip().lower() == "y":
        account.take_loan(kind, amount, months)
    else:
        info("Loan cancelled.")


def my_loans_menu(account):
    section("MY LOANS", "magenta")
    if not account.loans:
        info("You have no active loans.")
        return
    for n, l in enumerate(account.loans, 1):
        print(f"  {n}. {c(l.name, 'bold')}  ({l.rate * 100:g}% per year)")
        print(f"     Owed now : {c(rs(l.outstanding), 'red')}   EMI: {rs(l.emi)}")
    print(f"\n  Total owed: {c(rs(account.loan), 'red')}")

    pick = input("\n  Loan number to repay (Enter to go back): ").strip()
    if not pick:
        return
    if not pick.isdigit() or not 1 <= int(pick) <= len(account.loans):
        bad("Invalid loan number.")
        return
    loan = account.loans[int(pick) - 1]

    print(f"\n  Repay {loan.name}:")
    print(f"   1. Pay one EMI ({rs(min(loan.emi, loan.outstanding))})")
    print("   2. Pay a custom amount")
    print(f"   3. Pay in full ({rs(loan.outstanding)})")
    way = input("  Choose (1-3): ").strip()
    if way == "1":
        account.repay_loan(loan, min(loan.emi, loan.outstanding))
    elif way == "2":
        account.repay_loan(loan, get_amount("  Repay amount: Rs."))
    elif way == "3":
        account.repay_loan(loan, loan.outstanding)
    else:
        bad("Invalid choice.")