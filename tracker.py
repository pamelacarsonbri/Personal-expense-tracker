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
