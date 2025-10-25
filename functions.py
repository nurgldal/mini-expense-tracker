import json
import os
from datetime import datetime

DATA_FILE = "data.json"
CATEGORIES = ["Food", "Transportation", "Rent", "Shopping", "Bills", "Other"]

def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def ask_float(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Please enter a numeric value, e.g. 123.45")

def ask_date(prompt):
    while True:
        date_str = input(prompt) or datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")

def add_expense():
    data = read_data()
    id = len(data) + 1
    date = ask_date("Date (YYYY-MM-DD): ")
    
    print("\nAvailable categories:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"{i}. {cat}")

    while True:
        try:
            category_choice = int(input("Select a category number: "))
            if 1 <= category_choice <= len(CATEGORIES):
                category = CATEGORIES[category_choice - 1]
                break
            else:
                print("Invalid selection! Please choose a valid number.")
        except ValueError:
            print("Please enter a numeric value.")

    total = ask_float("Total amount (TL): ")
    explanation = input("Explanation: ")
    payment_type = input("Payment type (Cash/Card/Online): ")

    new_expense = {
        "id": id,
        "date": date,
        "category": category,
        "total": total,
        "explanation": explanation,
        "payment_type": payment_type
    }

    data.append(new_expense)
    save_data(data)
    print("✅ Expense added successfully!")

def list_expenses():
    data = read_data()
    if not data:
        print("No expenses have been added yet.")
        return
    for expense in data:
        print(f"[{expense['id']}] {expense['date']} - {expense['category']} - {expense['total']} TL - {expense['explanation']} ({expense['payment_type']})")

def delete_expense():
    data = read_data()
    if not data:
        print("No expenses to delete.")
        return

    delete_id = input("Enter the ID to delete: ")
    new_data = [e for e in data if str(e["id"]) != delete_id]

    if len(new_data) == len(data):
        print("No expense found with that ID.")
        return

    for i, expense in enumerate(new_data, start=1):
        expense["id"] = i

    save_data(new_data)
    print("❌ Expense deleted.")

def update_expense():
    data = read_data()
    if not data:
        print("No expenses to update.")
        return

    for expense in data:
        print(f"[{expense['id']}] {expense['date']} - {expense['category']} - {expense['total']} TL - {expense['explanation']} ({expense['payment_type']})")

    try:
        update_id = int(input("Enter the ID to update: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    expense_to_update = None
    for expense in data:
        if expense["id"] == update_id:
            expense_to_update = expense
            break

    if not expense_to_update:
        print("Expense not found.")
        return

    new_date = input(f"New date (current: {expense_to_update['date']}): ") or expense_to_update["date"]

    print("\nAvailable categories:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"{i}. {cat}")

    try:
        new_category_choice = input(f"Select new category number (current: {expense_to_update['category']}): ")
        if new_category_choice:
            new_category_choice = int(new_category_choice)
            if 1 <= new_category_choice <= len(CATEGORIES):
                new_category = CATEGORIES[new_category_choice - 1]
            else:
                print("Invalid category number. Keeping old category.")
                new_category = expense_to_update["category"]
        else:
            new_category = expense_to_update["category"]
    except ValueError:
        new_category = expense_to_update["category"]

    new_total_input = input(f"New total (current: {expense_to_update['total']}): ")
    if new_total_input:
        try:
            new_total = float(new_total_input)
        except ValueError:
            print("Invalid total value, keeping old one.")
            new_total = expense_to_update["total"]
    else:
        new_total = expense_to_update["total"]

    new_explanation = input(f"New explanation (current: {expense_to_update['explanation']}): ") or expense_to_update["explanation"]
    new_payment_type = input(f"New payment type (current: {expense_to_update['payment_type']}): ") or expense_to_update["payment_type"]

    expense_to_update.update({
        "date": new_date,
        "category": new_category,
        "total": new_total,
        "explanation": new_explanation,
        "payment_type": new_payment_type
    })

    save_data(data)
    print("✅ Expense updated successfully!")

def show_report():
    data = read_data()
    if not data:
        print("No expenses to report.")
        return

    totals_by_category = {}
    for expense in data:
        cat = expense["category"]
        total = expense["total"]
        totals_by_category[cat] = totals_by_category.get(cat, 0) + total

    print("\n--- Expense Report by Category ---")
    for cat, total in totals_by_category.items():
        print(f"{cat}: {total} TL")

def list_expenses_by_month():
    data = read_data()
    target_month = input("Enter month (YYYY-MM): ")

    filtered = [e for e in data if e["date"].startswith(target_month)]
    if not filtered:
        print("No expenses for that month.")
        return

    total_sum = 0
    for expense in filtered:
        print(f"[{expense['id']}] {expense['date']} - {expense['category']} - {expense['total']} TL - {expense['explanation']} ({expense['payment_type']})")
        total_sum += expense["total"]

    print(f"\nTotal for {target_month}: {total_sum} TL")
