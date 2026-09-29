from src.ui import banner, ok, bad, info, c, rs, WIDTH
from src.loan import MIN_OPENING, SAVINGS_RATE, INTEREST_TAX
from src.validation import get_amount
from src.account import Account
from src.banking import loan_menu, my_loans_menu

def main():
    print()
    banner("WELCOME TO LUMEN BANK")
    name = input("\n  Enter your name: ")

    while True:
        opening = get_amount("  Opening deposit: Rs.")
        if opening >= MIN_OPENING:
            break
        bad("That is too low to open an account. Try a (more than 10000) higher amount.")

    account = Account(name, opening)
    print()
    ok("Account opened successfully.")

    while True:
        print()
        banner(f"LUMEN BANK  -  {account.name}")
        print(f"  Balance: {c(rs(account.balance), 'green')}"
              f"    Loans due: {c(rs(account.loan), 'red') if account.loan else rs(0)}")
        print(c("  " + "─" * (WIDTH - 4), "dim"))
        print("  1. 💰 Deposit")
        print("  2. 💸 Withdraw")
        print("  3. 📊 Check balance")
        print("  4. 🏦 Apply for a loan (Home / Personal / Business / Education)")
        print("  5. 📋 My loans & repay")
        print("  6. ⏳ Let time pass (interest + tax)")
        print("  7. 🧾 Transaction history")
        print("  8. 🚪 Exit and print bill")
        print(c("  " + "─" * (WIDTH - 4), "dim"))

        choice = input("  Choose (1-8): ").strip()

        if choice == "1":
            account.deposit(get_amount())
        elif choice == "2":
            account.withdraw(get_amount())
        elif choice == "3":
            account.check_balance()
        elif choice == "4":
            loan_menu(account)
        elif choice == "5":
            my_loans_menu(account)
        elif choice == "6":
            info(f"Savings earn {SAVINGS_RATE * 100:.0f}% per year (tax {INTEREST_TAX * 100:.0f}% cut).")
            months = get_amount("  How many months should pass? (12 = 1 year): ")
            if 1 <= months <= 600:
                account.fast_forward(int(months))
            else:
                bad("Enter between 1 and 600 months.")
        elif choice == "7":
            account.show_history()
        elif choice == "8":
            if account.loans:
                print(c(f"  ! You still owe {rs(account.loan)} across {len(account.loans)} loan(s).", "yellow"))
            account.print_bill()
            input("\n  Press Enter to close the program...")
            break
        else:
            bad("Invalid choice, try again.")

        input("\n  Press Enter to continue...")

if __name__ == "__main__":
    main()