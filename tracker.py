   import datetime

categories = ["Food", "Transport", "Entertainment", "Utilities", "Health", "Other"]

def load_budgets():
    budgets = {}
    try:
        with open("budgets.txt", "r") as file:
            for line in file:
                category, amount = line.strip().split(",")
                budgets[category] = float(amount)
    except FileNotFoundError:
        pass
    return budgets

def save_budgets(budgets):
    with open("budgets.txt", "w") as file:
        for category, amount in budgets.items():
            file.write(f"{category},{amount}\n")

def load_expenses():
    expenses = []
    try:
        with open("expenses.txt", "r") as file:
            for line in file:
                date, category, description, amount = line.strip().split(",")
                expenses.append({
                    "date": date,
                    "category": category,
                    "description": description,
                    "amount": float(amount)
                })
    except FileNotFoundError:
        pass
    return expenses

def save_expenses(expenses):
    with open("expenses.txt", "w") as file:
        for e in expenses:
            file.write(f"{e['date']},{e['category']},{e['description']},{e['amount']}\n")

def set_budgets(budgets):
    for category in categories:
        amount = float(input(f"Enter monthly budget for {category}: "))
        budgets[category] = amount
    save_budgets(budgets)

def log_expense(expenses, budgets):
    category = input("Enter category: ")

    if category not in categories:
        print("Invalid category")
        return

    amount = float(input("Enter amount: "))
    description = input("Enter description: ")
    date = datetime.date.today()

    expense = {
        "date": str(date),
        "category": category,
        "description": description,
        "amount": amount
    }

    expenses.append(expense)
    save_expenses(expenses)

    # Budget warning
    total = sum(e["amount"] for e in expenses if e["category"] == category)

    if category in budgets and total > budgets[category]:
        print("⚠ WARNING: You are over your budget!")

def view_expenses(expenses):
    print("\nDate | Category | Description | Amount")
    print("-"*50)

    for e in expenses:
        print(f"{e['date']} | {e['category']} | {e['description']} | GHS {e['amount']:.2f}")


def category_summary(expenses, budgets):
    totals = {}

    for category in categories:
        totals[category] = 0

    for e in expenses:
        totals[e["category"]] += e["amount"]

    for category in categories:
        spent = totals[category]
        budget = budgets.get(category, 0)
        remaining = budget - spent

        print(f"\n{category}")
        print(f"Spent: GHS {spent:.2f}")
        print(f"Budget: GHS {budget:.2f}")
        print(f"Remaining: GHS {remaining:.2f}")

        if spent > budget:
            print(f"⚠ OVER BUDGET by GHS {spent-budget:.2f}")

def full_report(expenses):
    if not expenses:
        print("No expenses recorded.")
        return

    total = sum(e["amount"] for e in expenses)

    largest = max(expenses, key=lambda x: x["amount"])

    category_totals = {}
    for e in expenses:
        category_totals[e["category"]] = category_totals.get(e["category"], 0) + e["amount"]

    highest_category = max(category_totals, key=category_totals.get)

    print("\nFULL REPORT")
    print("Total spent:", total)
    print("Largest expense:", largest["description"], largest["amount"])
    print("Highest spending category:", highest_category)
    print("Number of expenses:", len(expenses))

def delete_expense(expenses):
    view_expenses(expenses)

    num = int(input("Enter expense number to delete: ")) - 1

    if 0 <= num < len(expenses):
        expenses.pop(num)
        save_expenses(expenses) 
        print("Expense deleted.")
    else:
        print("Invalid number.")


def main():
    budgets = load_budgets()
    expenses = load_expenses()

    while True:
        print("\nExpense Tracker")
        print("1. Set Budgets")
        print("2. Log Expense")
        print("3. View Expenses")
        print("4. Category Summary")
        print("5. Full Report")
        print("6. Delete Expense")
        print("7. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            set_budgets(budgets)

        elif choice == "2":
            log_expense(expenses, budgets)

        elif choice == "3":
            view_expenses(expenses)

        elif choice == "4":
            category_summary(expenses, budgets)

        elif choice == "5":
            full_report(expenses)

        elif choice == "6":
            delete_expense(expenses)

        elif choice == "7":
            break

        else:
            print("Invalid choice")

main()