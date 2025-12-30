import streamlit as st
from datetime import datetime

from utils import format_currency
from database import BudgetModel, CategoryModel


def render_budgets(budget_model: BudgetModel,
                   category_model: CategoryModel):
    st.title("💰 Budget Management")

    # Chọn tháng / năm cần xem
    today = datetime.today()
    col_m, col_y = st.columns(2)
    with col_m:
        month = st.number_input("Month", 1, 12, value=today.month, step=1)
    with col_y:
        year = st.number_input("Year", 2000, 2100, value=today.year, step=1)

    st.divider()

    col_form, col_list = st.columns([1, 2])

    # ------------------------------------
    # Form tạo / cập nhật budget
    # ------------------------------------
    with col_form:
        st.subheader("Create / Update Budget")

        # Có thể dùng dropdown category từ CategoryModel
        categories = [
            c["name"]
            for c in category_model.get_categories_by_type("Expense")
        ]
        category = st.selectbox(
            "Category",
            options=categories,
            index=0 if categories else None,
            placeholder="Select category...",
        )

        amount = st.number_input(
            "Budget amount",
            min_value=0.0,
            step=10.0,
            format="%.2f",
        )

        budget_type = st.selectbox(
            "Budget type",
            ["monthly", "weekly", "yearly"],
            index=0,
        )

        if st.button("Save budget", use_container_width=True):
            if not category:
                st.error("❌ Please select a category")
            elif amount <= 0:
                st.error("❌ Amount must be greater than 0")
            else:
                budget_model.create_budget(
                    category=category,
                    amount=amount,
                    budget_type=budget_type,
                    month=int(month),
                    year=int(year),
                )
                st.success("✅ Budget saved successfully!")

    # ------------------------------------
    # Danh sách budgets + progress bar
    # ------------------------------------
    with col_list:
        st.subheader("Budgets in this period")

        budgets = budget_model.get_budgets(
            month=int(month),
            year=int(year),
        )

        if not budgets:
            st.info("No budgets for this period.")
            return

        for b in budgets:
            progress = budget_model.get_budget_progress(
                category=b["category"],
                month=b["month"],
                year=b["year"],
            )

            used_pct = progress["percentage"]
            used_pct_display = min(used_pct, 100.0)
            spent = format_currency(progress["spent"])
            limit = format_currency(progress["budget"])
            remaining = format_currency(progress["remaining"])

            with st.container(border=True):
                st.write(f"**{b['category']}**  ({b['month']}/{b['year']})")
                st.write(f"Limit: {limit} | Spent: {spent} | Remaining: {remaining}")
                st.progress(
                    value=used_pct_display / 100.0,
                    text=f"{used_pct_display:.1f}% used",
                )

                # Nút xoá budget
                if st.button("Delete", key=f"del_budget_{b['_id']}"):
                    if budget_model.delete_budget(str(b["_id"])):
                        st.success("Budget deleted")
                    else:
                        st.error("Failed to delete budget")
