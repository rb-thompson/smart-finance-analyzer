import csv
from datetime import datetime
import logging

class FinanceUtils:
    """Class to manage financial transactions with CRUD operations and analysis."""

    def __init__(self):
        """Initialize transactions list and configure logging."""
        self.transactions = []
        # Configure logging to write to errors.txt
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='errors.txt',
            filemode='a'
        )

    def load_transactions(self, filename='financial transactions.csv'):
        """
        Load transactions from a CSV file into self.transactions.
        
        Args:
            filename (str): Path ro the CSV file.
            
        Returns:
            bool: True if loading succeeds, False otherwise.
        """
        self.transactions = []
        required_columns = {'transaction_id', 'date', 'customer_id', 'amount', 'type', 'description'}

        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Check required columns
                if not required_columns.issubset(reader.fieldnames):
                    missing = required_columns - set(reader.fieldnames)
                    logging.error(f"Missing columns in CSV: {missing}")
                    print(f"Missing columns in CSV: {missing}")
                    return False
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Validate transaction_id
                        try:
                            transaction_id = int(row['transaction_id'])
                        except ValueError:
                            logging.error(f"Row {row_num}: Invalid transaction_id '{row['transaction_id']}'")
                            continue

                        # Validate date
                        date_str = row['date'].strip()
                        try:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                        except ValueError:
                            logging.error(f"Row {row_num}: Invalid date format '{date_str}'")
                            continue

                        # Validate customer_id
                        try:
                            customer_id = int(row['customer_id'])
                        except ValueError:
                            logging.error(f"Row {row_num}: Invalid customer_id '{row['customer_id']}'")
                            continue

                        # Validate amount
                        try:
                            amount = float(row['amount'])
                            if amount < 0:
                                logging.error(f"Row {row_num}: Negative amount '{amount}'")
                                continue

                        except ValueError:
                            logging.error(f"Row {row_num}: Invalid amount '{row['amount']}'")
                            continue

                        # Validate type
                        transaction_type = row['type'].strip().lower()
                        if transaction_type not in {'credit', 'debit', 'transfer'}:
                            logging.error(f"Row {row_num}: Invalid transaction type '{transaction_type}'")
                            continue

                        # Adjust amount for debit
                        if transaction_type == 'debit':
                            amount = -amount

                        # Validate description
                        description = row['description'].strip()
                        if not description:
                            logging.error(f"Row {row_num}: Empty description")
                            continue

                        # Create transaction dictionary
                        transaction = {
                            'transaction_id': transaction_id,
                            'date': date_obj,
                            'customer_id': customer_id,
                            'amount': amount,
                            'type': transaction_type,
                            'description': description
                        }
                        self.transactions.append(transaction)

                    except KeyError as e:
                        logging.error(f"Row {row_num}: Missing column {e}")
                        continue

                print(f"Loaded {len(self.transactions)} transactions from '{filename}'.")
                return True
            
        except FileNotFoundError:
            logging.error(f"File '{filename}' not found.")
            print(f"File '{filename}' not found.")
            return False
        
        except csv.Error:
            logging.error(f"Malformed CSV file '{filename}'.")
            print(f"Error reading CSV file '{filename}'.")
            return False
        
        except IOError as e:
            logging.error(f"IO error reading {filename}: {e}")
            print(f"Error: IO error reading file: {e}")
            return False