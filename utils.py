import csv
from datetime import datetime
import logging
import os
from tabulate import tabulate

class FinanceUtils:
    """Class to manage financial transactions with CRUD operations and analysis."""

    def __init__(self):
        """Initialize transactions list and configure logging."""
        self.transactions = []
        # Configure logging with a custom FileHandler
        self.logger = logging.getLogger('FinanceUtils')
        self.logger.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        try:
            self.file_handler = logging.FileHandler('errors.txt', mode='a', encoding='utf-8')
            self.file_handler.setFormatter(formatter)
            self.logger.addHandler(self.file_handler)
        except IOError as e:
            print(f"Error: Cannot configure logging to errors.txt: {e}")
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            self.file_handler = None

    def __del__(self):
        """Ensure file handler is closed when instance is destroyed."""
        if hasattr(self, 'file_handler') and self.file_handler:
            self.file_handler.close()
            self.logger.removeHandler(self.file_handler)

    def _get_transaction_by_id(self, transaction_id):
        """Helper method to find a transaction by its ID."""
        for t in self.transactions:
            if t['transaction_id'] == transaction_id:
                return t
        return None

    def load_transactions(self, filename='financial_transactions.csv'):
        """
        Load transactions from a CSV file into self.transactions.
        
        Args:
            filename (str): Path to the CSV file.
            
        Returns:
            bool: True if loading succeeds, False otherwise.
        """
        self.transactions = []
        required_columns = {'transaction_id', 'date', 'customer_id', 'amount', 'type', 'description'}
        seen_ids = set()  # Track transaction_id duplicates

        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Check required columns
                if not required_columns.issubset(reader.fieldnames):
                    missing = required_columns - set(reader.fieldnames)
                    self.logger.error(f"Missing columns in CSV: {missing}")
                    print(f"Missing columns in CSV: {missing}")
                    return False
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Validate transaction_id
                        try:
                            transaction_id = int(row['transaction_id'])
                            if transaction_id in seen_ids:
                                self.logger.error(f"Row {row_num}: Duplicate transaction_id '{transaction_id}'")
                                continue
                            seen_ids.add(transaction_id)
                        except ValueError:
                            self.logger.error(f"Row {row_num}: Invalid transaction_id '{row['transaction_id']}'")
                            continue

                        # Validate date
                        date_str = row['date'].strip()
                        try:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                        except ValueError:
                            self.logger.error(f"Invalid date format: '{date_str}'")
                            continue

                        # Validate customer_id
                        try:
                            customer_id = int(row['customer_id'])
                            if customer_id <= 0:
                                self.logger.error(f"Non-positive customer_id: '{customer_id}'")
                                continue
                        except ValueError:
                            self.logger.error(f"Invalid customer_id: '{row['customer_id']}'")
                            continue

                        # Validate amount
                        try:
                            amount = float(row['amount'])
                            if amount < 0:
                                self.logger.error(f"Row {row_num}: Negative amount '{amount}'")
                                continue
                        except ValueError:
                            self.logger.error(f"Row {row_num}: Invalid amount '{row['amount']}'")
                            continue

                        # Validate type
                        transaction_type = row['type'].strip().lower()
                        if transaction_type not in {'credit', 'debit', 'transfer'}:
                            self.logger.error(f"Row {row_num}: Invalid transaction type '{transaction_type}'")
                            continue

                        # Adjust amount for debit
                        if transaction_type == 'debit':
                            amount = -amount

                        # Validate description
                        description = row.get('description')
                        if description is None or not str(description).strip():
                            self.logger.error(f"Row {row_num}: Empty description")
                            continue
                        description = str(description).strip()

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
                        self.logger.error(f"Row {row_num}: Missing column {e}")
                        continue

                if not self.transactions:
                    self.logger.error(f"No valid transactions in '{filename}'")
                    print(f"Error: No valid transactions in CSV")
                    return False
                
                print(f"Loaded {len(self.transactions)} transactions from '{filename}'.")

                # Create a backup of the original file and save it with a timestamp to /snapshots
                if not os.path.exists('snapshots'):
                    os.makedirs('snapshots')

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_filename = os.path.join('snapshots', f'backup_{timestamp}.csv')
                try:
                    with open(filename, 'rb') as src_file, open(backup_filename, 'wb') as dst_file:
                        dst_file.write(src_file.read())
                    print(f"Backup created: '{backup_filename}'")
                except Exception as e:
                    self.logger.error(f"Failed to create backup: {e}")
                    print(f"Warning: Failed to create backup: {e}")

                return True
            
        except FileNotFoundError:
            self.logger.error(f"File '{filename}' not found.")
            print(f"File '{filename}' not found.")
            return False
        
        except csv.Error:
            self.logger.error(f"Malformed CSV file '{filename}'.")
            print(f"Error reading CSV file '{filename}'.")
            return False
        
        except UnicodeDecodeError as e:
            self.logger.error(f"Encoding error in CSV file '{filename}': {e}")
            print(f"Error: Invalid encoding in CSV file")
            return False
        
        except IOError as e:
            self.logger.error(f"IO error reading {filename}: {e}")
            print(f"Error: IO error reading file: {e}")
            return False
        
    def add_transaction(self):
        print("\nAdd New Transaction (enter 'cancel' to abort)")

        # Date input
        while True:
            date_input = input("Enter date (YYYY-MM-DD): ").strip()
            if date_input.lower() == 'cancel':
                print("Transaction cancelled.")
                return False
            try:
                date_obj = datetime.strptime(date_input, '%Y-%m-%d').date()
                break
            except ValueError:
                self.logger.error(f"Invalid date format: {date_input}")
                print("Invalid date format. Please enter in YYYY-MM-DD format.")

        # Customer ID input with suggestions
        customer_ids = sorted(set(t['customer_id'] for t in self.transactions if t['customer_id'] > 0))
        if customer_ids:
            print(f"Valid customer IDs: {', '.join(map(str, customer_ids[:10]))}{'...' if len(customer_ids) > 10 else ''}")
        while True:
            customer_input = input("Enter customer ID (positive integer): ").strip()
            if customer_input.lower() == 'cancel':
                print("Transaction cancelled.")
                return False
            try:
                customer_id = int(customer_input)
                if customer_id <= 0:
                    self.logger.error(f"Non-positive customer ID input: {customer_input}")
                    print("Error: Customer ID must be a positive integer. Please try again.")
                    continue
                break
            except ValueError:
                self.logger.error(f"Invalid customer ID input: {customer_input}")
                print("Error: Customer ID must be an integer. Please try again.")

        # Amount input
        while True:
            amount_input = input("Enter amount (positive number): ").strip()
            if amount_input.lower() == 'cancel':
                print("Transaction cancelled.")
                return False
            try:
                amount = float(amount_input)
                if amount <= 0:
                    self.logger.error(f"Non-positive amount input: {amount_input}")
                    print("Error: Amount must be positive. Please try again.")
                    continue
                break
            except ValueError:
                self.logger.error(f"Invalid amount input: {amount_input}")
                print("Error: Amount must be a number. Please try again.")

        # Type input
        valid_types = ['credit', 'debit', 'transfer']  # Changed to sorted list
        while True:
            type_input = input("Enter type (credit/debit/transfer): ").strip().lower()
            if type_input.lower() == 'cancel':
                print("Transaction cancelled.")
                return False
            if type_input not in valid_types:
                self.logger.error(f"Invalid transaction type input: {type_input}")
                print(f"Error: Type must be one of {', '.join(valid_types)}. Please try again.")
                continue
            break

        # Adjust amount for debit
        if type_input == 'debit':
            amount = -amount

        # Description input
        while True:
            description = input("Enter description: (non-empty): ").strip()
            if description.lower() == 'cancel':
                print("Transaction cancelled.")
                return False
            if not description:
                self.logger.error("Empty description input")
                print("Error: Description cannot be empty. Please try again.")
                continue
            break

        # Generate new transaction ID
        transaction_id = max((t['transaction_id'] for t in self.transactions), default=0) + 1

        # Create and append transaction
        transaction = {
            'transaction_id': transaction_id,
            'date': date_obj,
            'customer_id': customer_id,
            'amount': amount,
            'type': type_input,
            'description': description
        }
        self.transactions.append(transaction)
        print(f"Transaction {transaction} added successfully!")
        return True

    def view_transactions(self, filter_type=None, filter_year=None):
        if not self.transactions:
            print("No transactions to display.")
            return False
        
        # Validate filter_type
        valid_types = ['credit', 'debit', 'transfer']  # Changed to sorted list
        if filter_type and filter_type.lower() not in valid_types:
            self.logger.error(f"Invalid filter type: {filter_type}")
            print(f"Error: Filter type must be one of {', '.join(valid_types)} or empty.")
            return False
        
        # Validate filter_year
        current_year = datetime.now().year
        if filter_year is not None:
            try:
                filter_year = int(filter_year)
                if not (1900 <= filter_year <= current_year):
                    self.logger.error(f"Invalid filter year: {filter_year}")
                    print(f"Error: Year must be between 1900 and {current_year}.")
                    return False
            except ValueError:
                self.logger.error(f"Invalid filter year input: {filter_year}")
                print("Error: Year must be an integer.")
                return False
            
        # Apply filters
        transactions = self.transactions
        if filter_type:
            transactions = [t for t in transactions if t['type'] == filter_type.lower()]
        if filter_year is not None:
            transactions = [t for t in transactions if t['date'].year == filter_year]

        if not transactions:
            filter_msg = f"{filter_type.capitalize()} transactions in {filter_year}" if filter_type and filter_year else \
                         f"{filter_type.capitalize()} transactions" if filter_type else \
                         f"All transactions in {filter_year}" if filter_year else "Transactions"
            print(f"No {filter_msg} found.")
            return False
        
        # Pagination
        page_size = 10
        total_pages = (len(transactions) + page_size - 1) // page_size
        current_page = 1

        while True:
            # Calculate slice for current page
            start_idx = (current_page - 1) * page_size
            end_idx = start_idx + page_size
            page_transactions = transactions[start_idx:end_idx]

            # Prepare table data
            table = [
                [
                    t['transaction_id'],
                    t['date'].strftime('%b %d, %Y'),
                    t['customer_id'],
                    f"${t['amount']:,.2f}",
                    t['type'].capitalize(),
                    t['description'][:30] + ('...' if len(t['description']) > 30 else '')
                ]
                for t in page_transactions
            ]

            headers = ['ID', 'Date', 'Customer', 'Amount', 'Type', 'Description']
            filter_msg = f"{filter_type.capitalize()} transactions in {filter_year}" if filter_type and filter_year else \
                         f"{filter_type.capitalize()} transactions" if filter_type else \
                         f"Transactions in {filter_year}" if filter_year else "All transactions"
            print(f"\n{filter_msg} (Page {current_page} of {total_pages}, {len(page_transactions)} transactions):")
            print(tabulate(table, headers=headers, tablefmt='grid', stralign='left'))

            # Navigation prompt
            if total_pages == 1:
                break
            print("\nEnter command (start, next, prev, end, exit):")
            command = input("> ").strip().lower()
            if command == 'exit':
                break
            elif command == 'start' and current_page > 1:
                current_page = 1
            elif command == 'next' and current_page < total_pages:
                current_page += 1
            elif command == 'prev' and current_page > 1:
                current_page -= 1
            elif command == 'end' and current_page < total_pages:
                current_page = total_pages
            else:
                print("Invalid command. Use 'start', 'next', 'prev', 'end', or 'exit'.")

        print(f"Displayed {len(transactions)} transactions across {total_pages} page(s).")
        return True
    
    def update_transaction(self):
        """
        Prompt user to update an existing transaction by ID.
        
        Returns:
            bool: True if transaction is updated, False if cancelled or invalid.
        """
        if not self.transactions:
            print("No transactions to update.")
            return False

        print("\nUpdate Transaction (enter 'cancel' to abort)")
        while True:
            id_input = input("Enter transaction ID (e.g., 100001): ").strip()
            if id_input.lower() == 'cancel':
                print("Update cancelled.")
                return False
            try:
                transaction_id = int(id_input)
                transaction = self._get_transaction_by_id(transaction_id)
                if not transaction:
                    self.logger.error(f"Transaction ID not found: '{transaction_id}'")
                    print(f"Error: Transaction ID {transaction_id} not found. Try again.")
                    continue
                break
            except ValueError:
                self.logger.error(f"Invalid transaction ID input: '{id_input}'")
                print("Error: Transaction ID must be an integer. Try again.")

        # Display current transaction
        print(f"\nUpdating Transaction {transaction_id}:")
        print(f"  Current: {transaction['date'].strftime('%Y-%m-%d')}, Customer {transaction['customer_id']}, "
              f"${abs(transaction['amount']):,.2f} {transaction['type'].capitalize()}, {transaction['description']}")
        print("Enter new values (press Enter to keep current, 'cancel' to abort)")

        # Date input
        while True:
            date_input = input(f"New date [{transaction['date'].strftime('%Y-%m-%d')}]: ").strip()
            if date_input.lower() == 'cancel':
                print("Update cancelled.")
                return False
            if not date_input:
                date_obj = transaction['date']
                break
            try:
                date_obj = datetime.strptime(date_input, '%Y-%m-%d').date()
                break
            except ValueError:
                self.logger.error(f"Invalid date input: '{date_input}'")
                print("Error: Date must be in YYYY-MM-DD format (e.g., 2020-10-26). Try again.")

        # Customer ID input
        customer_ids = sorted(set(t['customer_id'] for t in self.transactions if t['customer_id'] > 0))
        if customer_ids:
            print(f"Valid customer IDs: {', '.join(map(str, customer_ids[:10]))}{'...' if len(customer_ids) > 10 else ''}")
        while True:
            customer_input = input(f"New customer ID [{transaction['customer_id']}]: ").strip()
            if customer_input.lower() == 'cancel':
                print("Update cancelled.")
                return False
            if not customer_input:
                customer_id = transaction['customer_id']
                break
            try:
                customer_id = int(customer_input)
                if customer_id <= 0:
                    self.logger.error(f"Non-positive customer ID input: '{customer_id}'")
                    print("Error: Customer ID must be a positive integer. Try again.")
                    continue
                break
            except ValueError:
                self.logger.error(f"Invalid customer ID input: '{customer_input}'")
                print("Error: Customer ID must be a positive integer. Try again.")

        # Amount input
        while True:
            amount_input = input(f"New amount [{abs(transaction['amount']):,.2f}]: ").strip()
            if amount_input.lower() == 'cancel':
                print("Update cancelled.")
                return False
            if not amount_input:
                amount = abs(transaction['amount'])
                break
            try:
                amount = float(amount_input)
                if amount <= 0:
                    self.logger.error(f"Non-positive amount input: '{amount}'")
                    print("Error: Amount must be positive. Try again.")
                    continue
                break
            except ValueError:
                self.logger.error(f"Invalid amount input: '{amount_input}'")
                print("Error: Amount must be a number. Try again.")

        # Type input
        valid_types = {'credit', 'debit', 'transfer'}
        while True:
            type_input = input(f"New type [{transaction['type']}]: ").strip().lower()
            if type_input.lower() == 'cancel':
                print("Update cancelled.")
                return False
            if not type_input:
                type_input = transaction['type']
                break
            if type_input not in valid_types:
                self.logger.error(f"Invalid transaction type input: '{type_input}'")
                print(f"Error: Type must be one of {', '.join(valid_types)}. Try again.")
                continue
            break

        # Adjust amount for debit
        if type_input == 'debit':
            amount = -amount

        # Description input
        while True:
            description = input(f"New description [{transaction['description']}]: ").strip()
            if description.lower() == 'cancel':
                print("Update cancelled.")
                return False
            if not description:
                description = transaction['description']
                break
            if not description.strip():
                self.logger.error("Empty description input")
                print("Error: Description cannot be empty. Try again.")
                continue
            description = description.strip()
            break

        # Update transaction
        transaction.update({
            'date': date_obj,
            'customer_id': customer_id,
            'amount': amount,
            'type': type_input,
            'description': description
        })
        print(f"Transaction {transaction_id} updated successfully!")
        return True
    
    def delete_transaction(self):
        """
        Prompt user to delete a transaction by ID.
        
        Returns:
            bool: True if transaction is deleted, False if cancelled or invalid.
        """
        if not self.transactions:
            print("No transactions to delete.")
            return False

        print("\nDelete Transaction (enter 'cancel' to abort)")
        while True:
            id_input = input("Enter transaction ID (e.g., 123): ").strip()
            if id_input.lower() == 'cancel':
                print("Deletion cancelled.")
                return False
            try:
                transaction_id = int(id_input)
                transaction = self._get_transaction_by_id(transaction_id)
                if not transaction:
                    self.logger.error(f"Transaction ID not found: '{transaction_id}'")
                    print(f"Error: Transaction ID {transaction_id} not found. Try again.")
                    continue
                break
            except ValueError:
                self.logger.error(f"Invalid transaction ID input: '{id_input}'")
                print("Error: Transaction ID must be an integer. Try again.")

        # Display transaction
        print(f"\nTransaction to delete (ID {transaction_id}):")
        print(f"  {transaction['date'].strftime('%Y-%m-%d')}, Customer {transaction['customer_id']}, "
              f"${abs(transaction['amount']):,.2f} {transaction['type'].capitalize()}, {transaction['description']}")

        # Confirm deletion
        while True:
            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm == 'n' or confirm == 'cancel':
                print("Deletion cancelled.")
                return False
            if confirm == 'y':
                break
            print("Please enter 'y', 'n', or 'cancel'.")

        # Delete transaction
        self.transactions.remove(transaction)
        print(f"Transaction {transaction_id} deleted successfully!")
        return True
    
    def analyze_transactions(self):
        """
        Analyze transactions and print summary stats. 
        
        Save the analysis to analysis.txt
        """
        if not self.transactions:
            print("No transactions to analyze.")
            return False
        
        # Initialize analysis data
        type_sums = {"debit": 0.0, "credit": 0.0}
        transfer_total = 0.0

        # Process transactions
        for transaction in self.transactions:
            if transaction['type'] == 'debit':
                type_sums['debit'] += abs(transaction['amount'])
            elif transaction['type'] == 'credit':
                type_sums['credit'] += abs(transaction['amount'])
            elif transaction['type'] == 'transfer':
                transfer_total += abs(transaction['amount'])

        # Calculate totals
        total_transactions = len(self.transactions)
        total_debit = type_sums['debit']
        total_credit = type_sums['credit']
        total_transfer = transfer_total
        net_balance = total_credit + total_debit

        # Print summary
        print("\nFinancial Summary:")
        print(f"Total Credits: ${total_credit:,.2f}")
        print(f"Total Debits: ${total_debit:,.2f}")
        print(f"Total Transfers: ${total_transfer:,.2f}")
        print(f"Net Balance: ${net_balance:,.2f}")
        print(f"By type: ")
        for t in type_sums:
            print(f"  {t.capitalize()}: ${type_sums[t]:,.2f}")

        # Save analysis to file
        try:
            with open('analysis.txt', 'w', encoding='utf-8') as file:
                file.write("Financial Summary:\n")
                file.write(f"Total Credits: ${total_credit:,.2f}\n")
                file.write(f"Total Debits: ${total_debit:,.2f}\n")
                file.write(f"Total Transfers: ${total_transfer:,.2f}\n")
                file.write(f"Net Balance: ${net_balance:,.2f}\n")
                file.write("By type:\n")
                for t in type_sums:
                    file.write(f"  {t.capitalize()}: ${type_sums[t]:,.2f}\n")
            print("Analysis saved to 'analysis.txt'.")
        except IOError as e:
            self.logger.error(f"Failed to save analysis: {e}")
            print(f"Error: Failed to save analysis to 'analysis.txt': {e}")

        return True
    
    