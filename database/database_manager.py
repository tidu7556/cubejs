from pymongo import MongoClient, DESCENDING
import streamlit as st
import config


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _get_mongo_uri(self) -> str:
        # 1) Streamlit Cloud secrets (ưu tiên)
        if "MONGO_URI" in st.secrets:
            return st.secrets["MONGO_URI"]

        # 2) fallback local config (chạy ở máy bạn)
        return getattr(config, "MONGO_URI", None)

    def _get_db_name(self) -> str:
        # 1) có thể set trên secrets nếu muốn
        if "DATABASE_NAME" in st.secrets:
            return st.secrets["DATABASE_NAME"]

        # 2) fallback local config
        return getattr(config, "DATABASE_NAME", None)

    def _initialize(self):
        mongo_uri = self._get_mongo_uri()
        db_name = self._get_db_name()

        if not mongo_uri:
            raise ValueError("MONGO_URI is missing. Set it in Streamlit Secrets or config.py")
        if not db_name:
            raise ValueError("DATABASE_NAME is missing. Set it in Streamlit Secrets or config.py")

        # timeout để khỏi treo lâu trên Cloud
        self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
        self.db = self.client[db_name]

        try:
            self.db.command("ping")
            self._create_index()
            print("Initialize DB success")
        except Exception as e:
            print(f"Error in connect: {e}")
            raise

    def _create_index(self):
        self.db.transactions.create_index([("user_id", DESCENDING), ("date", DESCENDING)])
        self.db.categories.create_index(
            [("user_id", DESCENDING), ("type", DESCENDING), ("name", DESCENDING)],
            unique=True,
        )
        self.db.budgets.create_index(
            [("user_id", DESCENDING), ("category", DESCENDING), ("year", DESCENDING), ("month", DESCENDING)],
            unique=True,
        )

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def close_connection(self):
        if self.client:
            self.client.close()
            print("Shutdown database connection")
