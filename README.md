# Capstone Project: Smart Finance Analyzer

A command-line tool that manages financial transactions, generates reports, and provides insights into spending habits.

## Setup
1. Ensure Python 3 is installed.
2. Install the `tabulate` library: `pip install tabulate`.
3. Place `financial_transactions.csv` in the `/smart-finance-analyzer` directory.
4. Run the program with `python main.py`.

## Features
- Load transactions from `financial_transactions.csv`.
- Add new transactions with input validation and customer ID suggestions.
- View transactions in a formatted table, with optional type filtering.
- Analyze financial summaries (credits, debits, transfers, net balance) [TBD].
- Save transactions to CSV and generate a text report [TBD].

## Files
- `csv_faker.py` Generates dummy data for testing.
- `utils.py`: `FinanceUtils` class with core functionality.
- `main.py`: Menu-driven interface.
- `financial_transactions.csv`: Transaction data.
- `developer_transactions.csv`: Dummy data.
- `errors.txt`: Error log (generated).
- `report.txt`: Financial report (generated, TBD).
- `snapshots/`: Directory for CSV backups.

## Usage
Run `main.py` and select options 1–9. Ensure `financial_transactions.csv` is present before loading.