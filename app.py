import streamlit as st
import config

# import model
from database import (
    CategoryModel,
    TransactionModel,
    UserModel,
    BudgetModel,
)

# import analytics
from analytics.analyzer import FinanceAnalyzer
from analytics.visualizer import FinanceVisualizer

# import view module
from views import (
    render_categories,
    render_transactions,
    render_user_profile,
    render_dashboard,
    render_budgets,
)

# Page configuration (nên đặt trước khi render UI)
st.set_page_config(
    page_title="Finance Tracker",
    page_icon="🤑",
    layout="wide"
)

# initialize models
@st.cache_resource
def init_models():
    """Initialize and cached models"""
    return {
        "category": CategoryModel(),
        "transaction": TransactionModel(),
        "user": UserModel(),
        "visualizer": FinanceVisualizer(),
        "budget": BudgetModel(),
    }

# initialize session per user
if "models" not in st.session_state:
    st.session_state["models"] = init_models()

models = st.session_state["models"]

# =============================================
# 1. Authen User
# =============================================
def login_screen():
    st.header("This app is private")
    st.subheader("Please login to continue")
    st.button("Login with Google", on_click=st.login)

user = getattr(st, "user", None)
is_logged_in = bool(getattr(user, "is_logged_in", False))

if (user is None) or (not is_logged_in):
    login_screen()
    st.stop()

# Logged-in flow
user_model: UserModel = models["user"]
try:
    mongo_user_id = user_model.login(user.email)
except Exception as e:
    st.error(f"Error during user login: {e}")
    st.stop()

# =============================================
# 2. Set user context for models
# =============================================
models["category"].set_user_id(mongo_user_id)
models["transaction"].set_user_id(mongo_user_id)
models["budget"].set_user_id(mongo_user_id)

# =============================================
# 3. User profile
# =============================================
user_dict = user.to_dict()  # convert google user to dict
user_dict.update({"id": mongo_user_id})
render_user_profile(user_model, user_dict)

# init analyzer (transaction_model already has user_id)
analyzer_model = FinanceAnalyzer(models["transaction"])

# =============================================
# 4. Navigation
# =============================================
page = st.sidebar.radio("Navigation", ["Home", "Category", "Transaction", "Budget"])

# =============================================
# 5. Router
# =============================================
if page == "Home":
    st.title("Home")
    render_dashboard(
        analyzer_model=analyzer_model,
        transaction_model=models["transaction"],
        visualizer_model=models["visualizer"],
    )

elif page == "Category":
    render_categories(category_model=models["category"])

elif page == "Transaction":
    render_transactions(
        transaction_model=models["transaction"],
        category_model=models["category"],
    )

elif page == "Budget":
    render_budgets(
        budget_model=models["budget"],
        category_model=models["category"],
    )
