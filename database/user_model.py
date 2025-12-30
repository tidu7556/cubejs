from database.database_manager import DatabaseManager
import config
from datetime import datetime
from bson.objectid import ObjectId

collection_name = config.COLLECTIONS['user']

class UserModel:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.collection = self.db_manager.get_collection(collection_name=collection_name)
        self.transaction_collection = self.db_manager.get_collection(
            config.COLLECTIONS["transaction"]
        )
        self.category_collection = self.db_manager.get_collection(
            config.COLLECTIONS["category"]
        )
        self.budget_collection = self.db_manager.get_collection(
            config.COLLECTIONS["budget"]
        )
    def create_user(self, email: str) -> str:
        """Create new user"""

        user = {
            "email": email,
            "created_at": datetime.now(),
            "last_modified": datetime.now(),
            "is_activate": True
        }

        result = self.collection.insert_one(user)
        return str(result.inserted_id)
    
    def login(self, email: str) -> str:
        # check user exist (use find_one)
        user = self.collection.find_one({'email': email})
        
        # case 1: user not exist:
        # create: call create_user(email)
        if not user:
            return self.create_user(email)

        # case 2: user exist but deactivate
        # raise Error
        if user.get("is_activate") is not True:
            raise ValueError("This account is deactivated! Please connect to CS")

        # all checking passed
        return str(user.get("_id"))
    
    def deactivate_user(self, user_id: str) -> bool:
        # find and update:
        user = self.collection.find_one({
            "_id": ObjectId(user_id),
            "is_activate": True
        })

        # case: not exist user
        if not user:
            raise ValueError("User not found")
        
        # user is validate and ready to deactivate -> update them
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_activate": False}}
        )

        return result.modified_count > 0
    def delete_user_with_data(self, user_id: str) -> dict:
        oid = ObjectId(user_id)

        # 1. Xoá tất cả transactions của user
        tx_filter = {"user_id": oid}
        transactions_deleted = self.transaction_collection.count_documents(tx_filter)
        self.transaction_collection.delete_many(tx_filter)

        # 2. Xoá tất cả budgets của user
        budget_filter = {"user_id": oid}
        budgets_deleted = self.budget_collection.count_documents(budget_filter)
        self.budget_collection.delete_many(budget_filter)

        # 3. Xoá custom categories của user (giữ lại system defaults)
        default_names = set(
            config.DEFAULT_CATEGORIES_EXPENSE + config.DEFAULT_CATEGORIES_INCOME
        )

        category_filter = {
            "user_id": oid,
            "name": {"$nin": list(default_names)},  # chỉ xoá category không nằm trong default list
        }
        categories_deleted = self.category_collection.count_documents(category_filter)
        self.category_collection.delete_many(category_filter)

        # 4. Cuối cùng: xoá user document
        user_result = self.collection.delete_one({"_id": oid})
        user_deleted = user_result.deleted_count

        message = (
            f"Deleted: {user_deleted} user, "
            f"{transactions_deleted} transactions, "
            f"{budgets_deleted} budgets, "
            f"{categories_deleted} categories"
        )

        return {
            "user_deleted": user_deleted,
            "transactions_deleted": transactions_deleted,
            "budgets_deleted": budgets_deleted,
            "categories_deleted": categories_deleted,
            "message": message,
        }

