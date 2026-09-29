import os

# Let colors work on Windows terminals
os.system("")

WIDTH = 50
COLORS = {
    "red": "31", "green": "32", "yellow": "33", "blue": "34",
    "magenta": "35", "cyan": "36", "bold": "1", "dim": "2"
}

def c(text, color):
    return f"\033[{COLORS[color]}m{text}\033[0m"

def rs(x):
    return f"Rs.{x:,.2f}"

def time_text(months):
    return f"{months // 12} years {months % 12} months"

def banner(title, color="cyan"):
    print(c("╔" + "═" * (WIDTH - 2) + "╗", color))
    print(c("║", color) + title.center(WIDTH - 2) + c("║", color))
    print(c("╚" + "═" * (WIDTH - 2) + "╝", color))

def section(title, color="blue"):
    print("\n" + c(f"── {title} ".ljust(WIDTH, "─"), color))

def ok(msg):
    print(c(f"  ✔ {msg}", "green"))

def bad(msg):
    print(c(f"  ✘ {msg}", "red"))

def info(msg):
    print(c(f"  ℹ {msg}", "yellow"))