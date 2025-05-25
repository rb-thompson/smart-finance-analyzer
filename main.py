from utils import FinanceUtils

def main():
    """Main program for Smart Finance Analyzer."""
    finance = FinanceUtils()
    finance.clear_terminal()  # Clear terminal before showing menu

    # Optional colorama setup
    cyan = finance.color['cyan']
    green = finance.color['green']
    red = finance.color['red']
    reset = finance.color['reset']

    while True:
        print(f"\n{cyan}Smart Finance Analyzer{reset}")
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
                print(f"{green}Transactions loaded successfully.{reset}")
            else:
                print(f"{red}Failed to load transactions.{reset}")
        elif choice == '2':
            if finance.add_transaction():
                print(f"{green}Transaction added to memory. Save to persist changes.{reset}")
            else:
                print(f"Transaction not added.")
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
                print(f"{green}Transaction updated in memory. Save to persist changes.{reset}")
            else:
                print("Transaction not updated.")
        elif choice == '5':
            if finance.delete_transaction():
                print(f"{green}Transaction deleted from memory. Save to persist changes.{reset}")
            else:
                print("Transaction not deleted.")
        elif choice == '6':
            if finance.analyze_transactions():
                print(f"{green}Analysis complete.{reset}")
            else:
                print(f"{red}Analysis failed.{reset}")
        elif choice == '7':
            if finance.save_transactions():
                print(f"{green}Transactions saved successfully.{reset}")
            else:
                print(f"{red}Failed to save transactions.{reset}")
        elif choice == '8':
            if finance.generate_report():
                print(f"{green}Report generated successfully.{reset}")
            else:
                print(f"{red}Failed to generate report.{reset}")
        elif choice == '9':
            print(f"Exiting the program. {cyan}Goodbye!{reset}")
            break
        else:
            print("Invalid option or function not implemented.")

if __name__ == "__main__":
    main()