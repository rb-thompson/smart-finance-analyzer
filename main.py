from utils import FinanceUtils

def main():
    """Main program for Smart Finance Analyzer."""
    finance = FinanceUtils()

    while True:
        print("\nSmart Finance Analyzer")
        print("1. Load Transactions")
        print("2. Add Transaction")
        print("3. View Transactions")
        print("4. Update Transaction")
        print("5. Delete Transaction")
        print("6. Analyze Finances")
        print("7. Save Transactions")
        print("8. Generate Report")
        print("9. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            if finance.load_transactions():
                print("Transactions loaded successfully.")
            else:
                print("Failed to load transactions.")
        elif choice == '2':
            if finance.add_transaction():
                print("Transaction added to memory. Save to persist changes.")
            else:
                print("Transaction not added.")
        elif choice == '3':
            filter_type = input("Enter type to filter (credit/debit/transfer, or press Enter for all): ").strip()
            if not filter_type:
                filter_type = None
            filter_year = input("Enter year to filter (e.g., 2020, or press Enter for all): ").strip()
            if not filter_year:
                filter_year = None
            if not finance.view_transactions(filter_type, filter_year):
                print("No transactions displayed.")
        elif choice == '4':
            if finance.update_transaction():
                print("Transaction updated in memory. Save to persist changes.")
            else:
                print("Transaction not updated.")
        elif choice == '5':
            if finance.delete_transaction():
                print("Transaction deleted from memory. Save to persist changes.")
            else:
                print("Transaction not deleted.")
        elif choice == '6':
            if finance.analyze_transactions():
                print("Analysis complete. Check the report for details.")
            else:
                print("Analysis failed.")
        elif choice == '7':
            if finance.save_transactions():
                print("Transactions saved successfully.")
            else:
                print("Failed to save transactions.")
        elif choice == '8':
            if finance.generate_report():
                print("Report generated successfully.")
            else:
                print("Failed to generate report.")
        elif choice == '9':
            print("Exiting the program.")
            break
        else:
            print("Invalid option or function not implemented.")

if __name__ == "__main__":
    main()