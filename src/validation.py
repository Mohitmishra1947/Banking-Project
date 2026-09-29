from src.ui import bad

def get_amount(message="  Enter amount: Rs."):
    try:
        return float(input(message))
    except ValueError:
        bad("Please enter a number.")
        return 0