import csv
from datetime import datetime
import os

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the file paths
expenses_file = os.path.join(script_dir, 'expenses.csv')
budget_file = os.path.join(script_dir, 'budget.csv')

# Global variables
expenses = []
monthly_budget = None

def load_expenses(filename):
    """Load expenses from a CSV file."""
    expenses = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['amount'] = float(row['amount'])
                expenses.append(row)
    except FileNotFoundError:
        pass  # Start with an empty list if file doesn't exist
    return expenses

def load_budget(filename):
    """Load the budget from a file."""
    global monthly_budget
    try:
        with open(filename, 'r') as file:
            monthly_budget_value = file.readline().strip()
            if monthly_budget_value:
                monthly_budget = float(monthly_budget_value)
    except FileNotFoundError:
        pass  # Budget remains None if file doesn't exist

def save_expenses(filename, expenses):
    """Save the expenses list to a CSV file."""
    with open(filename, 'w', newline='') as file:
        fieldnames = ['date', 'category', 'amount', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for expense in expenses:
            writer.writerow(expense)

def save_budget(filename):
    """Save the budget to a file."""
    if monthly_budget is not None:
        with open(filename, 'w') as file:
            file.write(str(monthly_budget))

def add_expense():
    """Add a new expense to the expenses list."""
    while True:
        date_str = input("Enter the date (YYYY-MM-DD): ")
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    
    category = input("Enter the category: ").strip()
    
    while True:
        try:
            amount = float(input("Enter the amount: "))
            if amount <= 0:
                print("Amount must be positive.")
            else:
                break
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    description = input("Enter a description: ").strip()
    
    expense = {
        'date': date_str,
        'category': category,
        'amount': amount,
        'description': description
    }
    expenses.append(expense)
    print("Expense added successfully.")

def view_expenses():
    """Display all recorded expenses."""
    if not expenses:
        print("No expenses recorded.")
        return
    for expense in expenses:
        if all(key in expense for key in ['date', 'category', 'amount', 'description']):
            print(f"Date: {expense['date']}, Category: {expense['category']}, Amount: {expense['amount']:.2f}, Description: {expense['description']}")
        else:
            print("Incomplete expense entry found.")

def set_budget():
    """Set the monthly budget."""
    global monthly_budget
    while True:
        try:
            budget = float(input("Enter your monthly budget: "))
            if budget < 0:
                print("Budget cannot be negative.")
            else:
                monthly_budget = budget
                print(f"Monthly budget set to {monthly_budget:.2f}")
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

def track_budget():
    """Track spending against the monthly budget for the current month."""
    global monthly_budget
    if monthly_budget is None:
        print("Please set your monthly budget first.")
        set_budget()
        return
    
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    total = 0
    
    for expense in expenses:
        try:
            expense_date = datetime.strptime(expense['date'], "%Y-%m-%d")
            if expense_date.year == current_year and expense_date.month == current_month:
                total += expense['amount']
        except ValueError:
            print(f"Invalid date format for expense: {expense}")
            continue
    
    print(f"Monthly Budget: {monthly_budget:.2f}")
    print(f"Total Expenses (this month): {total:.2f}")
    if total > monthly_budget:
        excess = total - monthly_budget
        print(f"You have exceeded your budget by {excess:.2f}!")
    else:
        remaining = monthly_budget - total
        print(f"You have {remaining:.2f} left for the month.")

def main_menu():
    """Display an interactive menu and handle user choices."""
    while True:
        print("\nPersonal Expense Tracker")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Track budget")
        print("4. Save expenses and budget")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            track_budget()
        elif choice == '4':
            save_expenses(expenses_file, expenses)
            save_budget(budget_file)
            print("Expenses and budget saved successfully.")
        elif choice == '5':
            save_expenses(expenses_file, expenses)
            save_budget(budget_file)
            print("Expenses and budget saved. Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    expenses = load_expenses(expenses_file)
    load_budget(budget_file)
    main_menu()