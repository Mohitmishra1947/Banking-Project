from src.ui import section, c, rs, time_text, bad, info, banner
from src.loan import LOAN_TYPES, GST, emi_for
from src.validation import get_amount


def loan_menu(account):
    section("LOAN OFFERS", "magenta")

    print("  #  Type              Rate    Fee     Up to       Max time")

    for key in LOAN_TYPES:
        loan = LOAN_TYPES[key]

        print(
            " ",
            key,
            loan["name"],
            loan["rate"] * 100,
            "%",
            loan["fee"] * 100,
            "%",
            loan["limit"],
            "x balance",
            time_text(loan["max_months"])
        )

        print("    ", loan["icon"], loan["tag"])

    print("  0  Back")

    choice = input("\n  Choose loan type: ").strip()

    if choice == "0":
        return

    if choice not in LOAN_TYPES:
        bad("Invalid choice.")
        return

    kind = LOAN_TYPES[choice]

    room = account.room_for(kind)

    section(kind["name"].upper(), "magenta")

    print(
        "Interest rate:",
        kind["rate"] * 100,
        "% per year"
    )

    print(
        "Fee:",
        kind["fee"] * 100,
        "% +",
        GST * 100,
        "% GST"
    )

    print(
        "Minimum loan:",
        rs(kind["min"])
    )

    print(
        "You can borrow:",
        c(rs(room), "green")
    )

    if room < kind["min"]:
        bad(
            "Your balance is too low for this loan."
        )
        return

    amount = get_amount("Loan amount: Rs.")

    if amount < kind["min"]:
        bad(
            "Loan amount is below the minimum."
        )
        return

    if amount > room:
        bad(
            "You cannot borrow that much."
        )
        return

    months = get_amount(
        "Time in months: "
    )

    if months < 6 or months > kind["max_months"]:
        bad(
            "Invalid number of months."
        )
        return

    months = int(months)

    emi = emi_for(
        amount,
        kind["rate"],
        months
    )

    fee = round(
        amount * kind["fee"],
        2
    )

    gst = round(
        fee * GST,
        2
    )

    section("YOUR OFFER", "yellow")

    print(
        "Monthly EMI:",
        c(rs(emi), "yellow")
    )

    print(
        "Total to pay:",
        rs(emi * months)
    )

    print(
        "Fee + GST:",
        rs(fee + gst)
    )

    print(
        "You receive:",
        rs(amount - fee - gst)
    )

    answer = input(
        "\nConfirm this loan? (y/n): "
    ).strip().lower()

    if answer == "y":
        account.take_loan(
            kind,
            amount,
            months
        )
    else:
        info("Loan cancelled.")


def my_loans_menu(account):
    section("MY LOANS", "magenta")

    if not account.loans:
        info("You have no active loans.")
        return

    number = 1

    for loan in account.loans:

        print(
            number,
            ".",
            c(loan.name, "bold")
        )

        print(
            "   Interest:",
            loan.rate * 100,
            "% per year"
        )

        print(
            "   Owed:",
            c(rs(loan.outstanding), "red")
        )

        print(
            "   EMI:",
            rs(loan.emi)
        )

        number = number + 1

    print(
        "\nTotal owed:",
        c(rs(account.loan), "red")
    )

    choice = input(
        "\nLoan number to repay "
        "(Enter to go back): "
    ).strip()

    if choice == "":
        return

    if not choice.isdigit():
        bad("Invalid loan number.")
        return

    choice = int(choice)

    if choice < 1 or choice > len(account.loans):
        bad("Invalid loan number.")
        return

    loan = account.loans[choice - 1]

    print()
    print("Repay", loan.name)
    print(
        "1. Pay one EMI:",
        rs(min(loan.emi, loan.outstanding))
    )
    print("2. Pay a custom amount")
    print(
        "3. Pay in full:",
        rs(loan.outstanding)
    )

    way = input(
        "Choose 1, 2 or 3: "
    ).strip()

    if way == "1":

        amount = min(
            loan.emi,
            loan.outstanding
        )

        account.repay_loan(
            loan,
            amount
        )

    elif way == "2":

        amount = get_amount(
            "Repay amount: Rs."
        )

        account.repay_loan(
            loan,
            amount
        )

    elif way == "3":

        account.repay_loan(
            loan,
            loan.outstanding
        )

    else:
        bad("Invalid choice.")
