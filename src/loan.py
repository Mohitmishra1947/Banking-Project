MIN_OPENING = 10000   # required to open an account
SAVINGS_RATE = 0.04   # 4% interest per year on your balance
INTEREST_TAX = 0.10   # 10% tax (TDS) cut from savings interest
GST = 0.18            # 18% GST on the loan processing fee

# Each loan type has its own rate, fee, borrowing limit and time
LOAN_TYPES = {
    "1": {"name": "Home Loan",      "icon": "[HOME]",  "rate": 0.085, "fee": 0.005,
          "limit": 10, "min": 100000, "max_months": 240,
          "tag": "Lowest rate, longest time"},
    "2": {"name": "Personal Loan",  "icon": "[PERS]",  "rate": 0.12,  "fee": 0.02,
          "limit": 3,  "min": 10000,  "max_months": 60,
          "tag": "Quick cash for anything"},
    "3": {"name": "Business Loan",  "icon": "[BIZ ]",  "rate": 0.11,  "fee": 0.01,
          "limit": 6,  "min": 50000,  "max_months": 120,
          "tag": "Grow your business"},
    "4": {"name": "Education Loan", "icon": "[EDU ]",  "rate": 0.07,  "fee": 0.0025,
          "limit": 4,  "min": 20000,  "max_months": 180,
          "tag": "Invest in learning"},
}

def emi_for(principal, annual_rate, months):
    r = annual_rate / 12
    if r == 0:
        return principal / months
    return principal * r * (1 + r) ** months / ((1 + r) ** months - 1)


class Loan:
    def __init__(self, kind, principal, months):
        self.kind = kind
        self.name = kind["name"]
        self.rate = kind["rate"]
        self.principal = principal
        self.outstanding = principal
        self.months = months
        self.emi = round(emi_for(principal, self.rate, months), 2)