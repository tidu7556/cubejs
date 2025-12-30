import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "FINANCE-TRACKER"

# mongo configuration
MONGO_URI = os.getenv("MONGO_URI")  # không default localhost
DATABASE_NAME = os.getenv("DATABASE_NAME", "finance_tracker")

# collections
COLLECTIONS = {
    "user": "users",
    "transaction": "transactions",
    "category": "categories",
    "budget": "budgets"
}

# transaction types
TRANSACTION_TYPES = ['Expense', "Income"]

DEFAULT_CATEGORIES_EXPENSE = [
    "Shopping",
    "Transportation",
    "Entertainment",
    "Others"
]

DEFAULT_CATEGORIES_INCOME = [
    "Wave",
    "Others"
]

