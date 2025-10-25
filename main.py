from functions import *


def main():
    while True:
        print("\n--- Mini Expense Tracker ---")
        print("1. Add a new expense")
        print("2. View all expenses")
        print("3. Update an expense")
        print("4. Delete an expense")
        print("5. Show expense report")
        print("6. View expenses by month")
        print("7. Exit program")
        choice = input("Your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            list_expenses()
        elif choice == "3":
            update_expense()
            
        elif choice=="4":
            delete_expense()
            
        elif choice=="5":
            show_report()
            
        elif choice=="6":
            list_expenses_by_month()
            
        elif choice == "7":
             print("Exiting the program...")
             break
        else:
             print("Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
