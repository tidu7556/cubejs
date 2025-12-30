"""
pip install pymongo
python date1.py
"""

from pymongo import MongoClient
from datetime import datetime
import random

MONGO_URI = "mongodb+srv://<username>:<password>@cxxxxx.mongodb.net/?appName=Cluster0"

print("=" * 50)
print("CONNECT DB CONNECTION...")
print("=" * 50)

client = MongoClient(MONGO_URI)
db = client["finance_tracker"]
transactions = db["transactions"]

db.command("ping")
print("Database connect success")
print(f"Database name {db.name}")
print(f"First collection: {transactions.name}")


print("=" * 50)
print("INSERTING ONE TRANSACTION...")
print("=" * 50)

# Create a transaction document - dictionary
my_transaction = {
    "type": "Expense",
    "category": "Food",
    "amount": 25.50,
    "description": "Lunch at restaurant",
    "date": datetime.now(),
    "created_at": datetime.now()
}

# Insert the document
result = transactions.insert_one(my_transaction)

print(f"Transaction inserted!")
print(f"Generated ID: {result.inserted_id}")
print(f"Transaction details: {my_transaction}")
print()

print("=" * 50)
print("INSERTING MULTIPLE TRANSACTIONS...")
print("=" * 50)


# define whatever you want
TYPES = ["Expense", "Income"]
CATEGORIES = ["Shopping", "Coffee", "Travel"]

multi_transactions = []
for i in range(10):

    fake_trans = {
        "type": random.choice(TYPES),
        "category": random.choice(CATEGORIES),
        "amount": round(random.uniform(-10, 100), 2),
        "description": None, # <---- leave it empty for now
        "created_at": datetime.now()

    }
    multi_transactions.append(fake_trans)


result = transactions.insert_many(multi_transactions)
print(f"{len(result.inserted_ids)} transactions inserted!")
print(f"Generated _ids: {result.inserted_ids}")


print("=" * 50)
print("EMBEDDED DOCS INSERT...")
print("=" * 50)

my_emb_transaction = {
    "type": random.choice(TYPES),
    "amount": 1000,
    "description": "Shopping",
    "detail": [
        {
            "item": "shoes",
            "quantity": 1,
            "amount": 25.5,
            "discount": 50
        },
        {
            "item": "pant",
            "quantity": "5 kg",
            "amount": 5.25
        }
    ]
}

result = transactions.insert_one(my_emb_transaction)
print(f"Embedded docs inserted: {result.inserted_id}")

print("=" * 50)
print("READING ALL TRANSACTIONS...")
print("=" * 50)

# Find all transactions
all_transactions = transactions.find()

print(f"Total transactions in database:")
for transaction in all_transactions[:3]:
    print(f"  - {transaction.get('type')}: ${transaction.get('amount')} - {transaction.get('category')} - {transaction.get('description')}")

print()

print("=" * 50)
print("COUNTING DOCUMENTS...")
print("=" * 50)

total_count = transactions.count_documents({})
expense_count = transactions.count_documents({"type": "Expense"})
income_count = transactions.count_documents({"type": "Income"})

print(f"Statistics:")
print(f"  Total transactions: {total_count}")
print(f"  Expenses: {expense_count}")
print(f"  Income: {income_count}")
print()

print("=" * 50)
print("FILTERING TRANSACTIONS...")
print("=" * 50)

# Find only expenses
print("All Expenses:")
expenses = transactions.find({"type": "Expense"})
for expense in expenses:
    print(f"  - ${transaction.get('amount')} on {transaction.get('category')}: {transaction.get('description')}")

print()

# Find food expenses only
print("Food Expenses:")
food_expenses = transactions.find({"type": "Expense", "category": "Food"})
for food in food_expenses:
    print(f"  - ${food.get('amount')}: {food.get('description')}")

print()

# Find expenses greater than $20
print("Expenses > $20:")
big_expenses = transactions.find({"type": "Expense", "amount": {"$gt": 20}})
for expense in big_expenses:
    print(f"  - ${expense.get('amount')} on {expense.get('category')}: {expense.get('description')}")

print()

# Find invalid transaction: amount empty or < 0
print("Invalid transaction")
invalid_trans = transactions.find({
    "$or": [
        {"amount": {"$lt": 0}}, #$lt = less than
        {"amount": None},
        {"amount": ""}
    ]
})
for expense in invalid_trans:
    print(f"  - ${expense.get('amount')} on {expense.get('category')}: {expense.get('description')}")

print()