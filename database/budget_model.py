from datetime import datetime, date
from typing import Optional

from bson.objectid import ObjectId

from .database_manager import DatabaseManager
import config


class BudgetModel:
    def __init__(self, user_id: Optional[str] = None):
        self.db_manager = DatabaseManager()
        self.collection = self.db_manager.get_collection(
            config.COLLECTIONS["budget"]
        )
        self.transaction_collection = self.db_manager.get_collection(
            config.COLLECTIONS["transaction"]
        )
        self.user_id: Optional[ObjectId] = None
        if user_id:
            self.set_user_id(user_id)

    # -----------------------------
    # Helper
    # -----------------------------
    def set_user_id(self, user_id: Optional[str]):
        """Gắn user_id cho model (giống CategoryModel / TransactionModel)"""
        self.user_id = ObjectId(user_id) if user_id else None

    def _require_user(self):
        if not self.user_id:
            raise ValueError("user_id is required. Call set_user_id() first.")

    # -----------------------------
    # CRUD
    # -----------------------------
    def create_budget(
        self,
        category: str,
        amount: float,
        budget_type: str = "monthly",
        month: Optional[int] = None,
        year: Optional[int] = None,
    ) -> str:
        """Create (hoặc overwrite) budget cho 1 category / month / year."""

        self._require_user()

        if not month or not year:
            today = datetime.today()
            month = month or today.month
            year = year or today.year

        now = datetime.now()

        # upsert theo unique key (user, category, month, year)
        filter_ = {
            "user_id": self.user_id,
            "category": category,
            "month": month,
            "year": year,
        }

        update_doc = {
            "$set": {
                "budget_type": budget_type,
                "amount": amount,
                "updated_at": now,
            },
            "$setOnInsert": {
                "created_at": now,
            },
        }

        result = self.collection.update_one(filter_, update_doc, upsert=True)
        # Nếu insert mới -> result.upserted_id có giá trị, còn update thì None
        return str(result.upserted_id) if result.upserted_id else "updated"

    def get_budgets(
        self,
        month: Optional[int] = None,
        year: Optional[int] = None,
    ) -> list[dict]:
        """Lấy tất cả budgets của user (có thể filter theo month/year)."""

        self._require_user()

        query: dict = {"user_id": self.user_id}
        if month:
            query["month"] = month
        if year:
            query["year"] = year

        cursor = self.collection.find(query).sort(
            [("year", 1), ("month", 1), ("category", 1)]
        )
        return list(cursor)

    def update_budget(self, budget_id: str, new_amount: float) -> bool:
        """Update số tiền limit cho budget."""

        self._require_user()

        result = self.collection.update_one(
            {
                "_id": ObjectId(budget_id),
                "user_id": self.user_id,
            },
            {
                "$set": {
                    "amount": new_amount,
                    "updated_at": datetime.now(),
                }
            },
        )
        return result.modified_count > 0

    def delete_budget(self, budget_id: str) -> bool:
        """Xoá budget theo id (giới hạn theo user)."""

        self._require_user()

        result = self.collection.delete_one(
            {"_id": ObjectId(budget_id), "user_id": self.user_id}
        )
        return result.deleted_count > 0

    # -----------------------------
    # Progress with aggregation
    # -----------------------------
    def get_budget_progress(
        self,
        category: str,
        month: int,
        year: int,
    ) -> dict:
        """
        Tính progress của 1 budget bằng aggregation trên transactions.

        Return:
            {
                "budget": 500,
                "spent": 320,
                "remaining": 180,
                "percentage": 64.0
            }
        """

        self._require_user()

        # 1. Lấy budget amount
        budget_doc = self.collection.find_one(
            {
                "user_id": self.user_id,
                "category": category,
                "month": month,
                "year": year,
            }
        )
        if not budget_doc:
            return {
                "budget": 0,
                "spent": 0,
                "remaining": 0,
                "percentage": 0,
            }

        budget_amount = float(budget_doc.get("amount", 0))

        # 2. Tổng chi (Expense) trong tháng đó bằng aggregation
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        pipeline = [
            {
                "$match": {
                    "user_id": self.user_id,
                    "type": "Expense",
                    "category": category,
                    "date": {"$gte": start_date, "$lt": end_date},
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_spent": {"$sum": "$amount"},
                }
            },
        ]

        agg_result = list(self.transaction_collection.aggregate(pipeline))
        spent = float(agg_result[0]["total_spent"]) if agg_result else 0.0

        remaining = max(budget_amount - spent, 0.0)
        percentage = 0.0
        if budget_amount > 0:
            percentage = min(spent / budget_amount * 100, 999.9)

        return {
            "budget": budget_amount,
            "spent": spent,
            "remaining": remaining,
            "percentage": percentage,
        }
