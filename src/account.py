import os
from datetime import datetime

from src.ui import c, rs, time_text, banner, section, ok, bad, info
from src.loan import Loan, SAVINGS_RATE, INTEREST_TAX, GST


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BILLS_DIRECTORY = os.path.join(os.path.dirname(CURRENT_DIR), "bills here")


class Account:

    def __init__(self, name, opening_balance):
        self.name = name
        self.opening = opening_balance
        self.balance = opening_balance

        self.loans = []
        self.months = 0
        self.history = []

        self.deposited = 0
        self.withdrawn = 0
        self.interest = 0
        self.tax = 0

        self.loan_taken = 0
        self.loan_repaid = 0
        self.loan_interest = 0
        self.fees = 0
        self.gst = 0

    @property
    def loan(self):
        total = 0

        for loan in self.loans:
            total = total + loan.outstanding

        return total

    def deposit(self, amount):
        if amount <= 0:
            bad("Enter an amount greater than 0.")
            return

        self.balance = self.balance + amount
        self.deposited = self.deposited + amount

        self.history.append(("Deposit", amount, "+"))

        ok("Money deposited.")

    def withdraw(self, amount):
        if amount <= 0:
            bad("Enter an amount greater than 0.")
            return

        if amount > self.balance:
            bad("You don't have enough balance.")
            return

        self.balance = self.balance - amount
        self.withdrawn = self.withdrawn + amount

        self.history.append(("Withdrawal", amount, "-"))

        print()
        print("Withdrawal Slip")
        print("-----------------------------")
        print("Name  :", self.name)
        print("Date  :", datetime.now().strftime("%d-%m-%Y %H:%M"))
        print("Amount:", rs(amount))
        print("-----------------------------")

    def check_balance(self):
        section("ACCOUNT SUMMARY")

        print("Balance :", c(rs(self.balance), "green"))

        if self.loan > 0:
            print("Loans   :", c(rs(self.loan), "red"))
        else:
            print("Loans   :", rs(0))

        print("Net worth :", rs(self.balance - self.loan))
        print("Bank time :", time_text(self.months))

    def room_for(self, kind):
        borrowed = 0

        for loan in self.loans:
            if loan.kind is kind:
                borrowed = borrowed + loan.outstanding

        maximum = self.balance * kind["limit"]
        room = maximum - borrowed

        if room < 0:
            return 0

        return room

    def take_loan(self, kind, amount, months):
        fee = round(amount * kind["fee"], 2)
        gst = round(fee * GST, 2)

        new_loan = Loan(kind, amount, months)
        self.loans.append(new_loan)

        received = amount - fee - gst

        self.balance = self.balance + received
        self.loan_taken = self.loan_taken + amount
        self.fees = self.fees + fee
        self.gst = self.gst + gst

        self.history.append(
            (kind["name"] + " amount", amount, "+")
        )

        self.history.append(
            (kind["name"] + " fee", fee, "-")
        )

        self.history.append(
            ("GST on fee", gst, "-")
        )

        print()
        banner(kind["name"].upper() + " APPROVED", "green")

        print("Loan amount :", rs(amount))
        print("Fee         :", rs(fee))
        print("GST         :", rs(gst))
        print("Received    :", rs(received))
        print("Interest    :", kind["rate"] * 100, "%")
        print("Time        :", time_text(months))
        print("Monthly EMI :", rs(new_loan.emi))

    def repay_loan(self, loan, amount):
        if amount <= 0:
            bad("Enter an amount greater than 0.")
            return

        if amount > loan.outstanding + 0.005:
            bad("You cannot pay more than the loan amount.")
            return

        if amount > self.balance:
            bad("You don't have enough balance.")
            return

        self.balance = self.balance - amount
        loan.outstanding = loan.outstanding - amount
        self.loan_repaid = self.loan_repaid + amount

        self.history.append(
            (loan.name + " repayment", amount, "-")
        )

        ok("Loan repayment successful.")

        if loan.outstanding <= 0.005:
            self.loans.remove(loan)
            print(loan.name, "has been fully paid.")

    def fast_forward(self, months):
        total_interest = 0
        total_tax = 0
        total_loan_interest = 0

        for i in range(months):
            interest = round(
                self.balance * SAVINGS_RATE / 12,
                2
            )

            tax = round(
                interest * INTEREST_TAX,
                2
            )

            self.balance = self.balance + interest - tax

            total_interest = total_interest + interest
            total_tax = total_tax + tax

            for loan in self.loans:
                loan_interest = round(
                    loan.outstanding * loan.rate / 12,
                    2
                )

                loan.outstanding = (
                    loan.outstanding + loan_interest
                )

                total_loan_interest = (
                    total_loan_interest + loan_interest
                )

        self.months = self.months + months

        self.interest = self.interest + total_interest
        self.tax = self.tax + total_tax
        self.loan_interest = (
            self.loan_interest + total_loan_interest
        )

        if total_interest > 0:
            self.history.append(
                ("Savings interest", total_interest, "+")
            )

            self.history.append(
                ("Tax on interest", total_tax, "-")
            )

        if total_loan_interest > 0:
            self.history.append(
                ("Loan interest", total_loan_interest, "!")
            )

        section("TIME PASSED")

        print(months, "month(s) passed.")
        print("Savings interest:", rs(total_interest))
        print("Tax:", rs(total_tax))
        print("Loan interest:", rs(total_loan_interest))

    def show_history(self):
        section("TRANSACTION HISTORY")

        if not self.history:
            info("No transactions yet.")
            return

        number = 1

        for item in self.history:
            label = item[0]
            amount = item[1]
            sign = item[2]

            if sign == "+":
                text = "+" + rs(amount)

            elif sign == "-":
                text = "-" + rs(amount)

            else:
                text = "+" + rs(amount) + " added to loan"

            print(number, ".", label, text)

            number = number + 1

    def print_bill(self):
        now = datetime.now()

        rows = []

        rows.append("=" * 48)
        rows.append("LUMEN BANK - STATEMENT")
        rows.append("=" * 48)

        rows.append("Name      : " + self.name)

        rows.append(
            "Date      : " +
            now.strftime("%d-%m-%Y %H:%M")
        )

        rows.append(
            "Bank time : " +
            time_text(self.months)
        )

        rows.append("-" * 48)

        rows.append(
            "Opening balance : " +
            rs(self.opening)
        )

        for item in self.history:
            label = item[0]
            amount = item[1]
            sign = item[2]

            if sign == "!":
                sign = "*"

            rows.append(
                label + " " + sign + rs(amount)
            )

        rows.append("-" * 48)

        rows.append(
            "Total deposited : " +
            rs(self.deposited)
        )

        rows.append(
            "Total withdrawn : " +
            rs(self.withdrawn)
        )

        rows.append(
            "Savings interest: " +
            rs(self.interest)
        )

        rows.append(
            "Tax on interest : " +
            rs(self.tax)
        )

        rows.append(
            "Loans taken     : " +
            rs(self.loan_taken)
        )

        rows.append(
            "Loan interest   : " +
            rs(self.loan_interest)
        )

        rows.append(
            "Loan repaid     : " +
            rs(self.loan_repaid)
        )

        rows.append(
            "Loan fees + GST : " +
            rs(self.fees + self.gst)
        )

        if self.loans:
            rows.append("-" * 48)
            rows.append("LOANS STILL RUNNING")

            for loan in self.loans:
                rows.append(
                    loan.name + " " +
                    rs(loan.outstanding)
                )

        rows.append("-" * 48)

        rows.append(
            "Remaining balance : " +
            rs(self.balance)
        )

        rows.append(
            "Loans still due   : " +
            rs(self.loan)
        )

        rows.append(
            "Net worth         : " +
            rs(self.balance - self.loan)
        )

        rows.append("=" * 48)
        rows.append("Thanks for banking with us!")
        rows.append("=" * 48)

        statement = "\n".join(rows)

        print(statement)

        safe_name = ""

        for ch in self.name:
            if ch.isalnum():
                safe_name = safe_name + ch

        if safe_name == "":
            safe_name = "customer"

        filename = (
            "bill_" +
            safe_name +
            "_" +
            now.strftime("%Y%m%d_%H%M%S") +
            ".txt"
        )

        try:
            os.makedirs(
                BILLS_DIRECTORY,
                exist_ok=True
            )

            file_path = os.path.join(
                BILLS_DIRECTORY,
                filename
            )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(statement + "\n")

            ok("Bill saved as " + filename)

        except OSError:
            bad("Could not save the bill.")