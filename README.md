# Capstone Project: Smart Finance Analyzer

A command-line tool that manages financial transactions, generates reports, and provides insights into spending patterns.

## Setup
1. Ensure Python 3 is installed.
2. Install the `tabulate` library: `pip install tabulate`.
4. Run the program with `python main.py`.

## Features

- Load transactions from `financial_transactions.csv`, validating uniqueness of transaction IDs.
- Add transactions with input validation and customer ID suggestions.
- View transactions in a paginated table (10 per page), with filters for type (credit/debit/transfer) and year.
- Update transactions by ID, editing date, customer ID, amount, type, or description.
- Delete transactions by ID with confirmation.
- Analyze financial summaries (credits, debits, transfers, net balance).
- Save transactions to CSV and generate a text report.

## Bonus Features

- Creates timestamped backups of the input CSV in `snapshots/` on load.
- Supports year-based filtering for transaction views.
- Generates detailed reports with statistics.
- Uses [Tabulate](https://pypi.org/project/tabulate/) for formatted table output.
- Includes unit tests and a data-generator.

## Files

- `utils.py`: Contains `FinanceUtils` class with core logic for transaction management.
- `main.py`: Provides a menu-driven user interface.
- `financial_transactions.csv`: Stores transaction data.
- `errors.txt`: Logs errors during execution.
- `report.txt`: Outputs financial summary reports.
- `snapshots/`: Stores timestamped CSV backups.
- `csv_faker.py`: Generates test data using the Faker library (`pip install faker`).
- `test_finance_utils.py`: Runs unit tests for file handling and validation.

## Usage

1. Ensure `financial_transactions.csv` is in the project directory.
2. Run `python main.py` and select options 1–9 from the menu to manage transactions.

## Testing

- **Generate Test Data**: Run `python csv_faker.py` to create sample financial data tailored to a rural household.
- **Run Unit Tests**: Execute `python test_finance_utils.py` to verify functionality, with descriptive console output for each test.

## Author

Code by [R. Brandon Thompson](https://www.linkedin.com/in/appaltech/) 
Licensed under the MIT License.