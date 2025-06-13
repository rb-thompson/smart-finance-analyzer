# Capstone Project: Smart Finance Analyzer
A command-line tool that manages financial transactions, generates reports, and provides insights into spending patterns.

## 🚀 Getting Started  

### Prerequisites
- Python 3.12 or higher
- pip

### Quick Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/rb-thompson/smart-finance-analyzer.git
   cd smart-finance-analyzer
   ```  

2. **Set up virtual environment (Recommended)**  
   ```bash
   python -m venv venv

   source venv/bin/activate   # unix/macos

   venv\Scripts\activate   # windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```  
  
4. **Run the program**  
   ```bash
   python main.py
   ```

## ✨ Features

- Load transactions from `financial_transactions.csv`, validating uniqueness of transaction IDs.
- Add transactions with input validation and customer ID suggestions.
- View transactions in a paginated table (10 per page), with filters for type (credit/debit/transfer) and year.
- Update transactions by ID, editing date, customer ID, amount, type, or description.
- Delete transactions by ID with confirmation.
- Analyze financial summaries (credits, debits, transfers, net balance).
- Save transactions to CSV and generate a text report.
- Generate detailed financial reports saved to text files (`report_YYYYMMDD.txt`) including:
  - Date range and total transactions.
  - Financial summary (credits, debits, transfers, net balance).
  - Breakdown by transaction type (count and percentage).
  - Yearly and quarterly breakdowns (credits, debits, transfers, net balance, counts).
  - Top 5 customers by transaction volume.
  - Year-over-year growth for credits, debits, and net balance.
  - Anomaly detection for unusual transaction amounts (>3 standard deviations from mean).
- Logs errors to `errors.txt` and successful operations (load, save, add, update, delete, report) plus empty transaction attempts to `activity.txt`.
- Comprehensive input validation, error handling (e.g., file I/O, invalid data), and support for large datasets (e.g., 100,001 transactions).

### Bonus Features

- Creates timestamped backups of the input CSV in `snapshots/` on load.
- Supports year-based filtering for transaction views.
- Generates detailed reports with statistics.
- Uses [Tabulate](https://pypi.org/project/tabulate/) for formatted table output.
- Includes partial unit tests and a data-generator.

### Files

- `utils.py`: Contains `FinanceUtils` class with core logic for transaction management.
- `main.py`: Provides a menu-driven user interface.
- `financial_transactions.csv`: Stores transaction data.
- `logs/errors.txt`: Logs errors during execution.
- `logs/activity.txt`: Logs info messages and program operations.
- `reports/report_YYYYMMDD.txt`: Outputs time-stamped financial summary reports.
- `snapshots/backup_YYYYMMDD_TIME`: Stores timestamped CSV backups.
- `csv_faker.py`: Generates test data using the Faker library (`pip install faker`).
- `test_finance_utils.py`: Runs unit tests for file handling and validation [TBD].

## 📖 Usage

1. Ensure `financial_transactions.csv` is in the project directory.
2. Run `python main.py` and select options 1–9 from the menu to manage transactions.

## Author

Code by [R. Brandon Thompson](https://www.linkedin.com/in/appaltech/)  
Licensed under the MIT License.