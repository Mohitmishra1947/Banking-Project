# System Architecture - Lumen Bank

## Architecture Style
The Lumen Bank application follows a **Modular Monolith** architecture pattern. It separates concerns into clear, independent logical layers while maintaining execution within a single application process.

## Layer Breakdown
- **Presentation / UI Layer (`src/ui.py`, `src/banking.py`, `src/main.py`)**: Manages the command-line user interface, terminal color formatting, banners, interactive menus, and input prompts.
- **Business Logic Layer (`src/account.py`, `src/loan.py`)**: Houses core banking operations, account states, time-simulation engines, savings compound interest calculations, and EMI formulas.
- **Validation Layer (`src/validation.py`)**: Sanitizes and validates user input securely to prevent crashes.
- **Data Persistence**: Text-based itemized bill generation stored inside the `bills here/` directory.