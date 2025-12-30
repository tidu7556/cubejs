from database.database_manager import DatabaseManager
import config
from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId

collection_name = config.COLLECTIONS['category']

class CategoryModel:
    def __init__(self, user_id: Optional[str] = None):
        self.db_manager = DatabaseManager()
        self.collection = self.db_manager.get_collection(collection_name=collection_name)
        self.transaction_collection = self.db_manager.get_collection(
            config.COLLECTIONS["transaction"]
        )
        self.budget_collection = self.db_manager.get_collection(
            config.COLLECTIONS["budget"]
        )

        self.user_id = user_id
        # init:
        self.user_id = user_id

    def set_user_id(self, user_id: str):
        self.user_id = ObjectId(user_id) if user_id is not None else None

        # after we have user_id, initialize their default categories
        self._initialize_user_default_categories()

    def _initialize_user_default_categories(self):
        """Initialize user categories if they dont exist"""

        # Check if there is user_id, exist earlier
        if not self.user_id:
            return
        
        # EXPENSE
        for cate in config.DEFAULT_CATEGORIES_EXPENSE:
            # # calling by params order
            # self.upsert_category("Expense", cate)

            # calling by params keywords
            self.upsert_category(category_type = "Expense", category_name= cate)

        # INCOME
        for cate in config.DEFAULT_CATEGORIES_INCOME:
            self.upsert_category(category_type = "Income", category_name = cate)

    def upsert_category(self, category_type: str, category_name: str):

        # define filter
        filter_ = {
            "type": category_type,
            "name": category_name,
            "user_id": self.user_id
        }

        # define update_doc
        update_doc = {
            "$set": {
                "last_modified": datetime.now()
            },
            "$setOnInsert": {
                "created_at": datetime.now()
            } 
        }

        result = self.collection.update_one(
            filter_,
            update_doc,
            upsert=True
        )
        return result.upserted_id
    def update_category(
        self,
        category_id: str,
        new_type: str,
        new_name: str,
    ) -> dict:
        if not self.user_id:
            return {
                "updated": False,
                "affected": 0,
                "message": "user_id is not set for CategoryModel",
            }

        cat_id = ObjectId(category_id)

        # 1. Lấy category hiện tại
        current_cat = self.collection.find_one(
            {
                "_id": cat_id,
                "user_id": self.user_id,
            }
        )
        if not current_cat:
            return {
                "updated": False,
                "affected": 0,
                "message": "Category not found.",
            }

        old_name = current_cat.get("name")
        old_type = current_cat.get("type")

        new_name = new_name.strip()

        # 2. Không cho trùng tên trong cùng type + user
        duplicate = self.collection.find_one(
            {
                "user_id": self.user_id,
                "type": new_type,
                "name": new_name,
                "_id": {"$ne": cat_id},
            }
        )
        if duplicate:
            return {
                "updated": False,
                "affected": 0,
                "message": f"Category '{new_name}' already exists in {new_type}.",
            }

        name_changed = new_name != old_name
        type_changed = new_type != old_type

        # 3. Đếm transactions đang dùng category cũ
        tx_filter = {
            "user_id": self.user_id,
            "category": old_name,
        }
        affected = self.transaction_collection.count_documents(tx_filter)

        # 4. Nếu đổi type và còn transactions -> BLOCK
        if type_changed and affected > 0:
            return {
                "updated": False,
                "affected": affected,
                "message": (
                    f"Cannot change category type because {affected} "
                    "transactions are using this category."
                ),
            }

        # 5. Update chính category
        now = datetime.now()
        cat_update = {
            "$set": {
                "type": new_type,
                "name": new_name,
                "last_modified": now,
            }
        }

        cat_result = self.collection.update_one(
            {
                "_id": cat_id,
                "user_id": self.user_id,
            },
            cat_update,
        )

        if cat_result.modified_count == 0 and not name_changed and not type_changed:
            return {
                "updated": False,
                "affected": 0,
                "message": "No changes to update.",
            }

        # 6. Nếu có đổi tên -> update toàn bộ transactions liên quan
        updated_tx = 0
        if name_changed and affected > 0:
            tx_result = self.transaction_collection.update_many(
                tx_filter,
                {
                    "$set": {
                        "category": new_name,
                        "last_modified": now,
                    }
                },
            )
            updated_tx = tx_result.modified_count

        return {
            "updated": True,
            "affected": updated_tx,
            "message": f"Updated category and {updated_tx} related transactions",
        }

    def count_transactions_for_category(self, category_name: str) -> int:
    
        if not self.user_id:
            return 0

        filter_ = {
            "user_id": self.user_id,
            "category": category_name,
        }
        return self.transaction_collection.count_documents(filter_)
    def count_budgets_for_category(self, category_name: str) -> int:
        if not self.user_id:
            return 0

        filter_ = {
            "user_id": self.user_id,
            "category": category_name,
        }
        return self.budget_collection.count_documents(filter_)

    def delete_category(
        self,
        category_type: str,
        category_name: str,
        strategy: str = "block",
    ) -> dict:
        if not self.user_id:
            return {
                "deleted": False,
                "affected_transactions": 0,
                "affected_budgets": 0,
                "strategy": strategy,
                "message": "user_id is not set for CategoryModel",
            }

        # 1. Đếm số transaction bị ảnh hưởng
        tx_filter = {
            "user_id": self.user_id,
            "category": category_name,
        }
        affected_transactions = self.transaction_collection.count_documents(tx_filter)

        # 2. Đếm số budgets bị ảnh hưởng (Topic 5)
        budget_filter = {
            "user_id": self.user_id,
            "category": category_name,
        }
        affected_budgets = self.budget_collection.count_documents(budget_filter)

        # 3. Xử lý theo strategy
        if strategy == "block":
            if affected_transactions > 0 or affected_budgets > 0:
                return {
                    "deleted": False,
                    "affected_transactions": affected_transactions,
                    "affected_budgets": affected_budgets,
                    "strategy": "block",
                    "message": (
                        "Deletion blocked: "
                        f"{affected_transactions} transactions and "
                        f"{affected_budgets} budgets are still using this category."
                    ),
                }

        elif strategy == "reassign":
            now = datetime.now()
            # Reassign transactions sang 'Others'
            if affected_transactions > 0:
                self.transaction_collection.update_many(
                    tx_filter,
                    {
                        "$set": {
                            "category": "Others",
                            "last_modified": now,
                        }
                    },
                )
            # Budgets: xoá (tránh bị mồ côi)
            if affected_budgets > 0:
                self.budget_collection.delete_many(budget_filter)

        elif strategy == "cascade":
            # Xoá luôn transactions + budgets
            if affected_transactions > 0:
                self.transaction_collection.delete_many(tx_filter)
            if affected_budgets > 0:
                self.budget_collection.delete_many(budget_filter)

        # 4. Cuối cùng xoá category
        result = self.collection.delete_one(
            {
                "type": category_type,
                "name": category_name,
                "user_id": self.user_id,
            }
        )

        deleted = result.deleted_count > 0

        return {
            "deleted": deleted,
            "affected_transactions": affected_transactions,
            "affected_budgets": affected_budgets,
            "strategy": strategy,
            "message": "Category deleted successfully."
            if deleted
            else "Category not found or already deleted.",
        }

    def get_categories_by_type(self, category_type: str):
        """
        Lấy danh sách category theo type ('Expense' / 'Income') cho đúng user.
        """
        query = {
            "type": category_type,
            "user_id": self.user_id,
        }
        cursor = self.collection.find(query).sort("created_at", -1)
        return list(cursor)

    
    def get_total(self):
        result = self.collection.find({"user_id": self.user_id})
        result = list(result)
        return result

# if __name__ == "__main__":
#     print("Init cate collection")
#     cate = CategoryModel()

#     item = {
#         "type": "Expense",
#         "name": "Rent"
#     }

#     result = cate.add_category(category_type = "Expense", category_name="Rent")