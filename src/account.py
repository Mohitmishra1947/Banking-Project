import os
from datetime import datetime
from src.ui import c, rs, time_text, banner, section, ok, bad, info
from src.loan import Loan, SAVINGS_RATE, INTEREST_TAX, GST

FOLDER = os.path.dirname(os.path.abspath(__file__))
BILLS_FOLDER = os.path.join(os.path.dirname(FOLDER), "bills here")

class Account:
    def __init__(self, name, opening):
        self.name = name
        self.opening = opening
        self.balance = opening
        self.loans = []          
        self.months = 0          
        self.history = []        
        self.deposited = self.withdrawn = 0
        self.interest = self.tax = 0
        self.loan_taken = self.loan_repaid = self.loan_interest = 0
        self.fees = self.gst = 0

    @property
    def loan(self):
        return sum(l.outstanding for l in self.loans)

    def deposit(self, amount):
        if amount <= 0:
            bad("Amount must be more than 0.")
            return
        self.balance += amount
        self.deposited += amount
        self.history.append(("Deposit", amount, "+"))
        ok(f"Deposited {rs(amount)}")

    def withdraw(self, amount):
        if amount <= 0:
            bad("Amount must be more than 0.")
        elif amount > self.balance:
            bad("Not enough balance.")
        else:
            self.balance -= amount
            self.withdrawn += amount
            self.history.append(("Withdrawal", amount, "-"))
            print()
            print(c("  ┌" + "─" * 30 + "┐", "magenta"))
            print(c("  │", "magenta") + "        WITHDRAWAL SLIP       " + c("│", "magenta"))
            print(c("  ├" + "─" * 30 + "┤", "magenta"))
            for label, value in (("Name", self.name),
                                 ("Date", datetime.now().strftime('%d-%m-%Y %H:%M')),
                                 ("Amount", rs(amount))):
                print(c("  │", "magenta") + f" {label:<7}: {value:<20}" + c("│", "magenta"))
            print(c("  └" + "─" * 30 + "┘", "magenta"))

    def check_balance(self):
        section("ACCOUNT SUMMARY")
        print(f"  Balance    : {c(rs(self.balance), 'green')}")
        print(f"  Loans due  : {c(rs(self.loan), 'red') if self.loan else rs(0)}")
        print(f"  Net worth  : {c(rs(self.balance - self.loan), 'bold')}")
        print(f"  Bank time  : {time_text(self.months)}")

    def room_for(self, kind):
        used = sum(l.outstanding for l in self.loans if l.kind is kind)
        return max(self.balance * kind["limit"] - used, 0)

    def take_loan(self, kind, amount, months):
        fee = round(amount * kind["fee"], 2)
        gst = round(fee * GST, 2)
        loan = Loan(kind, amount, months)
        self.loans.append(loan)
        self.balance += amount - fee - gst
        self.loan_taken += amount
        self.fees += fee
        self.gst += gst
        self.history += [(f"{kind['name']} amount", amount, "+"),
                         (f"{kind['name']} fee", fee, "-"),
                         ("GST on fee", gst, "-")]
        print()
        banner(f"{kind['name'].upper()} APPROVED", "green")
        print(f"  Loan amount      : {rs(amount)}")
        print(f"  Processing fee   : {rs(fee)}  ({kind['fee'] * 100:g}%)")
        print(f"  GST on fee       : {rs(gst)}  ({GST * 100:.0f}%)")
        print(f"  Credited to you  : {c(rs(amount - fee - gst), 'green')}")
        print(f"  Interest rate    : {kind['rate'] * 100:g}% per year")
        print(f"  Time             : {time_text(months)}")
        print(f"  Monthly EMI      : {c(rs(loan.emi), 'yellow')}")

    def repay_loan(self, loan, amount):
        if amount <= 0:
            bad("Amount must be more than 0.")
        elif amount > loan.outstanding + 0.005:
            bad(f"You only owe {rs(loan.outstanding)} on this loan.")
        elif amount > self.balance:
            bad("Not enough balance to repay that much.")
        else:
            amount = min(amount, loan.outstanding)
            self.balance -= amount
            loan.outstanding -= amount
            self.loan_repaid += amount
            self.history.append((f"{loan.name} repayment", amount, "-"))
            ok(f"Repaid {rs(amount)} on your {loan.name}")
            if loan.outstanding <= 0.005:
                self.loans.remove(loan)
                print(c(f"  ★ Congratulations! Your {loan.name} is fully paid off! ★", "green"))

    def fast_forward(self, months):
        earned = taxed = loan_int = 0
        for _ in range(months):
            i = round(self.balance * SAVINGS_RATE / 12, 2)
            t = round(i * INTEREST_TAX, 2)
            self.balance += i - t
            earned += i
            taxed += t
            for l in self.loans:
                li = round(l.outstanding * l.rate / 12, 2)
                l.outstanding += li
                loan_int += li
        self.months += months
        self.interest += earned
        self.tax += taxed
        self.loan_interest += loan_int
        if earned:
            self.history.append((f"Savings interest ({months} mo)", earned, "+"))
            self.history.append(("Tax on interest (10%)", taxed, "-"))
        if loan_int:
            self.history.append((f"Loan interest ({months} mo)", loan_int, "!"))
        section("TIME PASSED")
        print(f"  {months} month(s) passed. Bank time is now {time_text(self.months)}.")
        print(f"  Savings interest earned : {c('+' + rs(earned), 'green')}")
        print(f"  Tax cut (10%)           : {c('-' + rs(taxed), 'red')}")
        print(f"  Loan interest added     : {c(rs(loan_int), 'yellow')}")

    def show_history(self):
        section("TRANSACTION HISTORY")
        if not self.history:
            info("No transactions yet.")
        for i, (label, amount, sign) in enumerate(self.history, 1):
            if sign == "+":
                shown = c(f"+{rs(amount)}", "green")
            elif sign == "-":
                shown = c(f"-{rs(amount)}", "red")
            else:
                shown = c(f"+{rs(amount)} (added to loan)", "yellow")
            print(f"  {i:>2}. {label:<30} {shown}")

    def print_bill(self):
        now = datetime.now()
        line = "=" * 48
        rows = [
            "", line, "            LUMEN BANK - BILL", line,
            f"  Name       : {self.name}",
            f"  Date       : {now.strftime('%d-%m-%Y %H:%M')}",
            f"  Bank time  : {time_text(self.months)}",
            "-" * 48,
            f"  {'Opening balance':<30} {rs(self.opening):>15}",
        ]
        for label, amount, sign in self.history:
            shown = "*" if sign == "!" else sign
            rows.append(f"  {label:<30}{shown}{rs(amount):>15}")
        rows += [
            "  * added to your loans, not your balance",
            "-" * 48,
            f"  {'Total deposited':<30} {rs(self.deposited):>15}",
            f"  {'Total withdrawn':<30} {rs(self.withdrawn):>15}",
            f"  {'Savings interest earned':<30} {rs(self.interest):>15}",
            f"  {'Tax on interest':<30} {rs(self.tax):>15}",
            f"  {'Loans taken':<30} {rs(self.loan_taken):>15}",
            f"  {'Loan interest charged':<30} {rs(self.loan_interest):>15}",
            f"  {'Loan repaid':<30} {rs(self.loan_repaid):>15}",
            f"  {'Loan fees + GST':<30} {rs(self.fees + self.gst):>15}",
        ]
        if self.loans:
            rows.append("-" * 48)
            rows.append("  LOANS STILL RUNNING")
            for l in self.loans:
                rows.append(f"  {l.name:<30} {rs(l.outstanding):>15}")
        rows += [
            "-" * 48,
            f"  {'REMAINING BALANCE':<30} {rs(self.balance):>15}",
            f"  {'LOANS STILL DUE':<30} {rs(self.loan):>15}",
            f"  {'NET WORTH':<30} {rs(self.balance - self.loan):>15}",
            line, "   Thank you for banking with us!", line,
        ]
        text = "\n".join(rows)
        print(c(text, "cyan"))

        safe = "".join(ch for ch in self.name if ch.isalnum()) or "customer"
        filename = f"bill_{safe}_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            os.makedirs(BILLS_FOLDER, exist_ok=True)
            with open(os.path.join(BILLS_FOLDER, filename), "w", encoding="utf-8") as f:
                f.write(text + "\n")
            ok(f"Bill saved in the 'bills here' folder as {filename}")
        except OSError:
            bad("Could not save the bill file.")