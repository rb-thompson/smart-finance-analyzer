import unittest
from unittest.mock import patch
import io
import os
import time
import csv
from datetime import datetime
from utils import FinanceUtils
import logging


class TestFinanceUtils(unittest.TestCase):
    def setUp(self):
        """Set up a FinanceUtils instance and a small test CSV."""
        # Clear test_errors.txt
        if os.path.exists('test_errors.txt'):
            try:
                os.remove('test_errors.txt')
            except PermissionError:
                time.sleep(0.1)
                os.remove('test_errors.txt')
        # Create FinanceUtils instance with test-specific logging
        self.finance = FinanceUtils()
        if self.finance.file_handler:
            self.finance.file_handler.close()
            self.finance.logger.removeHandler(self.finance.file_handler)
        # Configure test-specific logging
        self.finance.file_handler = logging.FileHandler('test_errors.txt', mode='w', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.finance.file_handler.setFormatter(formatter)
        self.finance.logger.addHandler(self.finance.file_handler)
        # Create test CSV (for consistency, though not read)
        self.test_csv = "test_transactions.csv"
        self.test_data = [
            {
                'transaction_id': '1',
                'date': '2020-10-26',
                'customer_id': '926',
                'amount': '6478.39',
                'type': 'credit',
                'description': 'Online purchase - Electronics'
            },
            {
                'transaction_id': '2',
                'date': '2020-10-27',
                'customer_id': '466',
                'amount': '100.50',
                'type': 'debit',
                'description': 'Grocery shopping'
            },
            {
                'transaction_id': '3',
                'date': '2021-03-15',
                'customer_id': '123',
                'amount': '2500.00',
                'type': 'transfer',
                'description': 'Savings account transfer'
            },
            {
                'transaction_id': '4',
                'date': '2021-06-20',
                'customer_id': '926',
                'amount': '89.99',
                'type': 'debit',
                'description': 'Streaming subscription'
            },
            {
                'transaction_id': '5',
                'date': '2022-01-10',
                'customer_id': '789',
                'amount': '4500.00',
                'type': 'credit',
                'description': 'Freelance payment'
            },
            {
                'transaction_id': '6',
                'date': '2022-01-11',
                'customer_id': '789',
                'amount': '200.00',
                'type': 'debit',
                'description': 'Utility bill'
            },
            {
                'transaction_id': '7',
                'date': '2022-09-05',
                'customer_id': '466',
                'amount': '1200.00',
                'type': 'transfer',
                'description': 'Investment account deposit'
            },
            {
                'transaction_id': '8',
                'date': '2023-02-14',
                'customer_id': '123',
                'amount': '75.25',
                'type': 'debit',
                'description': 'Restaurant dinner'
            },
            {
                'transaction_id': '9',
                'date': '2023-07-30',
                'customer_id': '926',
                'amount': '3000.00',
                'type': 'credit',
                'description': 'Salary deposit'
            },
            {
                'transaction_id': '10',
                'date': '2023-08-01',
                'customer_id': '466',
                'amount': '150.00',
                'type': 'debit',
                'description': 'Phone bill'
            },
            {
                'transaction_id': '11',
                'date': '2024-04-12',
                'customer_id': '789',
                'amount': '600.00',
                'type': 'transfer',
                'description': 'Charity donation'
            },
            {
                'transaction_id': '12',
                'date': '2024-05-20',
                'customer_id': '123',
                'amount': '45.00',
                'type': 'debit',
                'description': 'Coffee shop'
            },
            {
                'transaction_id': '13',
                'date': '2024-11-25',
                'customer_id': '926',
                'amount': '800.00',
                'type': 'credit',
                'description': 'Bonus payment'
            },
            {
                'transaction_id': '14',
                'date': '2025-01-15',
                'customer_id': '466',
                'amount': '500.00',
                'type': 'transfer',
                'description': 'Loan repayment'
            },
            {
                'transaction_id': '15',
                'date': '2025-02-10',
                'customer_id': '789',
                'amount': '299.99',
                'type': 'debit',
                'description': 'New headphones'
            }
        ]
        with open(self.test_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['transaction_id', 'date', 'customer_id', 'amount', 'type', 'description'])
            writer.writeheader()
            writer.writerows(self.test_data)
        # Manually populate self.finance.transactions instead of load_transactions
        self.finance.transactions = []
        for row in self.test_data:
            transaction = {
                'transaction_id': int(row['transaction_id']),
                'date': datetime.strptime(row['date'], '%Y-%m-%d').date(),
                'customer_id': int(row['customer_id']),
                'amount': float(row['amount']) * (-1 if row['type'] == 'debit' else 1),
                'type': row['type'].lower(),
                'description': row['description'].strip()
            }
            self.finance.transactions.append(transaction)

    def tearDown(self):
        """Clean up test files and close logging handler."""
        if hasattr(self, 'finance') and hasattr(self.finance, 'file_handler') and self.finance.file_handler:
            self.finance.file_handler.close()
            self.finance.logger.removeHandler(self.finance.file_handler)
        if os.path.exists(self.test_csv):
            try:
                os.remove(self.test_csv)
            except PermissionError:
                time.sleep(0.1)
                os.remove(self.test_csv)
        if os.path.exists('test_errors.txt'):
            try:
                os.remove('test_errors.txt')
            except PermissionError:
                time.sleep(0.1)
                os.remove('test_errors.txt')
        snapshots = 'snapshots'
        if os.path.exists(snapshots):
            for f in os.listdir(snapshots):
                try:
                    os.remove(os.path.join(snapshots, f))
                except PermissionError:
                    time.sleep(0.1)
                    os.remove(os.path.join(snapshots, f))
            try:
                os.rmdir(snapshots)
            except PermissionError:
                time.sleep(0.1)
                os.rmdir(snapshots)
        if hasattr(self, 'finance'):
            del self.finance

    def read_errors_txt(self):
        """Read test_errors.txt content."""
        try:
            with open('test_errors.txt', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ""

class TestAddTransaction(TestFinanceUtils):
    @patch('builtins.input', side_effect=[
        '2025-05-21', '926', '100.50', 'credit', 'Test purchase'
    ])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_transaction(self, mock_stdout, mock_input):
        """Test 2.1: Add a valid transaction."""
        result = self.finance.add_transaction()
        self.assertTrue(result)
        self.assertEqual(len(self.finance.transactions), 16)  # 15 + 1
        new_transaction = self.finance.transactions[-1]
        self.assertEqual(new_transaction['transaction_id'], 16)  # Next ID after 15
        self.assertEqual(new_transaction['date'], datetime(2025, 5, 21).date())
        self.assertEqual(new_transaction['customer_id'], 926)
        self.assertEqual(new_transaction['amount'], 100.50)
        self.assertEqual(new_transaction['type'], 'credit')
        self.assertEqual(new_transaction['description'], 'Test purchase')
        self.assertIn("Transaction {'transaction_id': 16", mock_stdout.getvalue())
        self.assertEqual(self.read_errors_txt(), "")

    @patch('builtins.input', side_effect=['2025-13-01', 'cancel'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_invalid_date(self, mock_stdout, mock_input):
        """Test 2.2: Invalid date input."""
        result = self.finance.add_transaction()
        self.assertFalse(result)
        self.assertEqual(len(self.finance.transactions), 15)  # No change
        self.assertIn("Invalid date format. Please enter in YYYY-MM-DD format.", mock_stdout.getvalue())
        self.assertIn("Transaction cancelled.", mock_stdout.getvalue())
        self.assertIn("Invalid date format: 2025-13-01", self.read_errors_txt())

    @patch('builtins.input', side_effect=['2025-05-21', '-1', 'cancel'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_negative_customer_id(self, mock_stdout, mock_input):
        """Test 2.3: Negative customer ID."""
        result = self.finance.add_transaction()
        self.assertFalse(result)
        self.assertEqual(len(self.finance.transactions), 15)  # No change
        self.assertIn("Error: Customer ID must be a positive integer. Please try again.", mock_stdout.getvalue())
        self.assertIn("Non-positive customer ID input: -1", self.read_errors_txt())

    @patch('builtins.input', side_effect=['2025-05-21', 'abc', 'cancel'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_invalid_customer_id(self, mock_stdout, mock_input):
        """Test 2.4: Invalid customer ID."""
        result = self.finance.add_transaction()
        self.assertFalse(result)
        self.assertEqual(len(self.finance.transactions), 15)  # No change
        self.assertIn("Error: Customer ID must be an integer. Please try again.", mock_stdout.getvalue())
        self.assertIn("Invalid customer ID input: abc", self.read_errors_txt())

    @patch('builtins.input', side_effect=['2025-05-21', '926', '-100', 'cancel'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_non_positive_amount(self, mock_stdout, mock_input):
        """Test 2.5: Non-positive amount."""
        result = self.finance.add_transaction()
        self.assertFalse(result)
        self.assertEqual(len(self.finance.transactions), 15)  # No change
        self.assertIn("Error: Amount must be positive. Please try again.", mock_stdout.getvalue())
        self.assertIn("Non-positive amount input: -100", self.read_errors_txt())

    @patch('builtins.input', side_effect=['2025-05-21', '926', '100.50', 'invalid', 'cancel'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_invalid_type(self, mock_stdout, mock_input):
        """Test 2.6: Invalid transaction type."""
        result = self.finance.add_transaction()
        self.assertFalse(result)
        self.assertEqual(len(self.finance.transactions), 15)  # No change
        self.assertIn("Error: Type must be one of credit, debit, transfer. Please try again.", mock_stdout.getvalue())
        self.assertIn("Invalid transaction type input: invalid", self.read_errors_txt())

    @patch('builtins.input', side_effect=['2025-05-21', '926', '100.50', 'credit', '', 'cancel'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_empty_description(self, mock_stdout, mock_input):
        """Test 2.7: Empty description."""
        result = self.finance.add_transaction()
        self.assertFalse(result)
        self.assertEqual(len(self.finance.transactions), 15)  # No change
        self.assertIn("Error: Description cannot be empty. Please try again.", mock_stdout.getvalue())
        self.assertIn("Empty description input", self.read_errors_txt())

    @patch('builtins.input', side_effect=['2025-05-21', '926', '100.50', 'credit', 'Test'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_customer_id_suggestions(self, mock_stdout, mock_input):
        """Test 2.8: Customer ID suggestions."""
        self.finance.add_transaction()
        self.assertIn("Valid customer IDs: 123, 466, 789, 926", mock_stdout.getvalue())  # All customer IDs
        self.assertEqual(len(self.finance.transactions), 16)  # 15 + 1

    @patch('builtins.input', side_effect=[
        '2025-05-21', '926', '100.50', 'credit', 'Test1',
        '2025-05-22', '466', '200.75', 'debit', 'Test2'
    ])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_multiple_transactions(self, mock_stdout, mock_input):
        """Test 2.9: Add multiple transactions."""
        self.finance.add_transaction()
        self.finance.add_transaction()
        self.assertEqual(len(self.finance.transactions), 17)  # 15 + 2
        self.assertEqual(self.finance.transactions[-2]['transaction_id'], 16)  # First added
        self.assertEqual(self.finance.transactions[-1]['transaction_id'], 17)  # Second added
        self.assertIn("Transaction {'transaction_id': 16", mock_stdout.getvalue())
        self.assertIn("Transaction {'transaction_id': 17", mock_stdout.getvalue())

class TestViewTransactions(TestFinanceUtils):
    @patch('builtins.input', side_effect=['exit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_view_all_transactions(self, mock_stdout, mock_input):
        """Test 3.1: View all transactions."""
        result = self.finance.view_transactions()
        self.assertTrue(result)
        output = mock_stdout.getvalue()
        self.assertIn("All transactions (Page 1 of 2, 10 transactions)", output)  # 15 transactions, 2 pages
        self.assertIn("Oct 26, 2020", output)
        self.assertIn("$6,478.39", output)
        self.assertIn("Credit", output)
        self.assertIn("Online purchase - Electronics", output)  # Updated description
        self.assertIn("Displayed 15 transactions across 2 page(s)", output)
        self.assertEqual(self.read_errors_txt(), "")

    @patch('builtins.input', side_effect=['exit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_type_filter_credit(self, mock_stdout, mock_input):
        """Test 3.2: Filter by type (credit)."""
        result = self.finance.view_transactions(filter_type='credit')
        self.assertTrue(result)
        output = mock_stdout.getvalue()
        self.assertIn("Credit transactions (Page 1 of 1, 4 transactions)", output)  # 4 credits
        self.assertIn("926", output)
        self.assertIn("789", output)
        self.assertNotIn("466", output)  # 466 has debit/transfer
        self.assertEqual(self.read_errors_txt(), "")

    @patch('builtins.input', side_effect=['exit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_year_filter_2020(self, mock_stdout, mock_input):
        """Test 3.3: Filter by year (2020)."""
        result = self.finance.view_transactions(filter_year=2020)
        self.assertTrue(result)
        output = mock_stdout.getvalue()
        self.assertIn("Transactions in 2020 (Page 1 of 1, 2 transactions)", output)
        self.assertIn("926", output)
        self.assertIn("466", output)
        self.assertNotIn("789", output)
        self.assertEqual(self.read_errors_txt(), "")

    @patch('builtins.input', side_effect=['exit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_type_and_year_filter(self, mock_stdout, mock_input):
        """Test 3.4: Filter by type and year."""
        result = self.finance.view_transactions(filter_type='debit', filter_year=2020)
        self.assertTrue(result)
        output = mock_stdout.getvalue()
        self.assertIn("Debit transactions in 2020 (Page 1 of 1, 1 transactions)", output)
        self.assertIn("466", output)
        self.assertNotIn("926", output)
        self.assertEqual(self.read_errors_txt(), "")

    @patch('builtins.input', side_effect=['next', 'prev', 'exit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pagination_navigation(self, mock_stdout, mock_input):
        """Test 3.5: Pagination navigation."""
        for i in range(16, 26):  # IDs 16-25
            self.finance.transactions.append({
                'transaction_id': i,
                'date': datetime(2020, 10, 28).date(),
                'customer_id': 100 + i,
                'amount': 50.0,
                'type': 'credit',
                'description': f'Test {i}'
            })
        result = self.finance.view_transactions()
        self.assertTrue(result)
        output = mock_stdout.getvalue()
        self.assertIn("Page 1 of 3", output)  # 25 transactions, 3 pages
        self.assertIn("Page 2 of 3", output)
        self.assertIn("Enter command (start, next, prev, end, exit):", output)
        self.assertIn("Displayed 25 transactions across 3 page(s)", output)
        self.assertEqual(self.read_errors_txt(), "")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_invalid_type_filter(self, mock_stdout):
        """Test 3.6: Invalid type filter."""
        result = self.finance.view_transactions(filter_type='invalid')
        self.assertFalse(result)
        output = mock_stdout.getvalue()
        self.assertIn("Error: Filter type must be one of credit, debit, transfer or empty.", output)
        self.assertIn("Invalid filter type: invalid", self.read_errors_txt())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_invalid_year_filter(self, mock_stdout):
        """Test 3.7: Invalid year filter."""
        result = self.finance.view_transactions(filter_year=1800)
        self.assertFalse(result)
        output = mock_stdout.getvalue()
        self.assertIn("Error: Year must be between 1900 and", output)
        self.assertIn("Invalid filter year: 1800", self.read_errors_txt())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_non_integer_year(self, mock_stdout):
        """Test 3.8: Non-integer year."""
        result = self.finance.view_transactions(filter_year='abc')
        self.assertFalse(result)
        output = mock_stdout.getvalue()
        self.assertIn("Error: Year must be an integer.", output)
        self.assertIn("Invalid filter year input: abc", self.read_errors_txt())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_no_matching_transactions(self, mock_stdout):
        """Test 3.9: No matching transactions."""
        result = self.finance.view_transactions(filter_type='credit', filter_year=2019)
        self.assertFalse(result)
        output = mock_stdout.getvalue()
        self.assertIn("No Credit transactions in 2019 found.", output)
        self.assertEqual(self.read_errors_txt(), "")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_empty_transactions(self, mock_stdout):
        """Test 3.10: Empty transactions list."""
        self.finance.transactions = []
        result = self.finance.view_transactions()
        self.assertFalse(result)
        output = mock_stdout.getvalue()
        self.assertIn("No transactions to display.", output)
        self.assertEqual(self.read_errors_txt(), "")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_single_page(self, mock_stdout):
        """Test 3.11: Single page with few transactions."""
        self.finance.transactions = [self.finance.transactions[0]]
        result = self.finance.view_transactions()
        self.assertTrue(result)
        output = mock_stdout.getvalue()
        self.assertIn("All transactions (Page 1 of 1, 1 transactions)", output)
        self.assertNotIn("Enter command (start, next, prev, end, exit)", output)
        self.assertIn("Displayed 1 transactions across 1 page(s)", output)
        self.assertEqual(self.read_errors_txt(), "")

    @patch('builtins.input', side_effect=['2025-05-21', '926', '100.50', 'credit', 'A' * 100, 'next', 'exit'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_long_description(self, mock_stdout, mock_input):
        """Test 3.12: Long description truncation."""
        self.finance.add_transaction()
        # Capture add_transaction output
        add_output = mock_stdout.getvalue()
        self.assertIn("Transaction {'transaction_id': 16", add_output)  # Next ID after 15
        self.assertIn('A' * 100, add_output)  # Full description in add_transaction
        # Reset stdout for view_transactions
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        result = self.finance.view_transactions()
        self.assertTrue(result)
        view_output = mock_stdout.getvalue()
        self.assertIn("A" * 30 + "...", view_output)
        self.assertNotIn("A" * 100, view_output)
        self.assertEqual(self.read_errors_txt(), "")

class TestUpdateTransaction(TestFinanceUtils):
    @patch('builtins.input', side_effect=[
        '1',          # transaction_id
        '2025-05-22', # new date
        '466',        # new customer_id
        '200.75',     # new amount
        'debit',      # new type
        'Updated'     # new description
    ])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_update(self, mock_stdout, mock_input):
        """Test 4.1: Update a valid transaction."""
        result = self.finance.update_transaction()
        self.assertTrue(result)
        transaction = self.finance._get_transaction_by_id(1)
        self.assertEqual(transaction['date'], datetime(2025, 5, 22).date())
        self.assertEqual(transaction['customer_id'], 466)
        self.assertEqual(transaction['amount'], -200.75)
        self.assertEqual(transaction['type'], 'debit')
        self.assertEqual(transaction['description'], 'Updated')
        self.assertIn("Transaction 1 updated successfully!", mock_stdout.getvalue())
        self.assertEqual(self.read_errors_txt(), "")

    @patch('builtins.input', side_effect=['999', 'cancel'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_invalid_id(self, mock_stdout, mock_input):
        """Test 4.2: Invalid transaction ID."""
        result = self.finance.update_transaction()
        self.assertFalse(result)
        self.assertIn("Error: Transaction ID 999 not found. Try again.", mock_stdout.getvalue())
        self.assertIn("Transaction ID not found: '999'", self.read_errors_txt())

    @patch('builtins.input', side_effect=['1', '2025-13-01', 'cancel'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_invalid_date(self, mock_stdout, mock_input):
        """Test 4.3: Invalid date input."""
        result = self.finance.update_transaction()
        self.assertFalse(result)
        self.assertIn("Error: Date must be in YYYY-MM-DD format (e.g., 2020-10-26). Try again.", mock_stdout.getvalue())
        self.assertIn("Invalid date input: '2025-13-01'", self.read_errors_txt())

    @patch('builtins.input', side_effect=['1', '', '', '', '', ''])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_keep_existing_values(self, mock_stdout, mock_input):
        """Test 4.4: Keep existing transaction values."""
        original = self.finance._get_transaction_by_id(1).copy()
        result = self.finance.update_transaction()
        self.assertTrue(result)
        transaction = self.finance._get_transaction_by_id(1)
        self.assertEqual(transaction, original)
        self.assertIn("Transaction 1 updated successfully!", mock_stdout.getvalue())
        self.assertEqual(self.read_errors_txt(), "")

    @patch('builtins.input', side_effect=['cancel'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cancel_update(self, mock_stdout, mock_input):
        """Test 4.5: Cancel update."""
        result = self.finance.update_transaction()
        self.assertFalse(result)
        self.assertIn("Update cancelled.", mock_stdout.getvalue())
        self.assertEqual(self.read_errors_txt(), "")

class TestDeleteTransaction(TestFinanceUtils):
    @patch('builtins.input', side_effect=['1', 'y'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_delete(self, mock_stdout, mock_input):
        """Test 5.1: Delete a valid transaction."""
        result = self.finance.delete_transaction()
        self.assertTrue(result)
        self.assertEqual(len(self.finance.transactions), 14)  # 15 - 1
        self.assertIsNone(self.finance._get_transaction_by_id(1))
        self.assertIn("Transaction 1 deleted successfully!", mock_stdout.getvalue())
        self.assertEqual(self.read_errors_txt(), "")

    @patch('builtins.input', side_effect=['999', 'cancel'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_invalid_id(self, mock_stdout, mock_input):
        """Test 5.2: Invalid transaction ID."""
        result = self.finance.delete_transaction()
        self.assertFalse(result)
        self.assertIn("Error: Transaction ID 999 not found. Try again.", mock_stdout.getvalue())
        self.assertIn("Transaction ID not found: '999'", self.read_errors_txt())

    @patch('builtins.input', side_effect=['1', 'n'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cancel_delete(self, mock_stdout, mock_input):
        """Test 5.3: Cancel deletion."""
        result = self.finance.delete_transaction()
        self.assertFalse(result)
        self.assertEqual(len(self.finance.transactions), 15)  # No change
        self.assertIn("Deletion cancelled.", mock_stdout.getvalue())
        self.assertEqual(self.read_errors_txt(), "")

if __name__ == '__main__':
    unittest.main()