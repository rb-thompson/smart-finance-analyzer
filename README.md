# Capstone Project: Smart Finance Analyzer

A command-line tool that manages financial transactions, generates reports, and provides insights into spending habits.

## Setup
1. Ensure Python 3 is installed.
2. Install the `tabulate` library: `pip install tabulate`.
3. Place `financial_transactions.csv` in the `/smart-finance-analyzer` directory.
4. Run the program with `python main.py`.

## Features
- Load transactions from `financial_transactions.csv`, validating uniqueness of transaction IDs.
- Add transactions with input validation and customer ID suggestions.
- View transactions in a paginated table (10 per page), with filters for type (credit/debit/transfer) and year.
- Update transactions by ID, editing date, customer ID, amount, type, or description.
- Delete transactions by ID with confirmation.
- Analyze financial summaries (credits, debits, transfers, net balance) [TBD].
- Save transactions to CSV and generate a text report [TBD].

## Bonus Features
- Creates timestamped backups of the input CSV in `snapshots/`.
- Supports year-based filtering in transaction viewing.

## Files
- `csv_faker.py` Generates dummy data for testing.
- `utils.py`: `FinanceUtils` class with core functionality.
- `main.py`: Menu-driven interface.
- `financial_transactions.csv`: Transaction data.
- `test_transactions.csv`: Testing data.
- `errors.txt`: Error log (generated).
- `report.txt`: Financial report (generated, TBD).
- `snapshots/`: Directory for CSV backups.

## Usage
Run `main.py` and select options 1–9. Ensure `financial_transactions.csv` is present before loading.