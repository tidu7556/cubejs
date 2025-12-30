import streamlit as st
import config

# function to render category list
def _render_category_list(category_model, category_type: str):
    st.subheader(f"{category_type} Categories")
    expense_lst = category_model.get_categories_by_type(category_type = category_type)

    if expense_lst:
        st.write(f"Total: {len(expense_lst)} categories")
        st.write("")

        cols = st.columns(3)

        for idx, item in enumerate(expense_lst):
            col_idx = idx % 3 # remaining fraction

            with cols[col_idx]:
                with st.container():
                    subcol_a, subcol_b = st.columns([4, 1])

                    with subcol_a:
                        st.write(f"📌 {item.get('name')}")
                        created_at = item.get("created_at")
                        if created_at:
                            try:
                                st.caption(created_at.strftime("%d-%m-%Y"))
                            except Exception:
                                st.caption(str(created_at))

                        # Edit: rename + change type
                        with st.expander("Edit", expanded=False):
                            new_name = st.text_input(
                                "Name",
                                value=item.get("name"),
                                key=f"edit_name_{item['_id']}",
                            )
                            new_type = st.selectbox(
                                "Type",
                                options=config.TRANSACTION_TYPES,
                                index=0
                                if item.get("type") == config.TRANSACTION_TYPES[0]
                                else 1,
                                key=f"edit_type_{item['_id']}",
                            )

                            if st.button(
                                "Save changes",
                                key=f"save_cat_{item['_id']}",
                                use_container_width=True,
                            ):
                                result = category_model.update_category(
                                    category_id=str(item["_id"]),
                                    new_type=new_type,
                                    new_name=new_name,
                                )

                                if result.get("updated"):
                                    st.success(result.get("message"))
                                    st.rerun()
                                else:
                                    st.error(result.get("message"))

                        with subcol_b:
                            strategy_label = st.selectbox(
                                "Delete strategy",
                                [
                                    "Block if has related transactions",
                                    "Reassign related transactions to 'Others'",
                                    "Delete related transactions (cascade)",
                                ],
                                key=f"strategy_{item['_id']}",
                            )

                            delete_button = st.button("❌", key=f"del_cat_{item['_id']}")
                            if delete_button:
                                name = item.get("name")

                                # Đếm cả transactions & budgets
                                tx_affected = category_model.count_transactions_for_category(
                                    category_name=name
                                )
                                budget_affected = category_model.count_budgets_for_category(
                                    category_name=name
                                )

                                # Warning chi tiết (Topic 2 + 5)
                                if tx_affected > 0 or budget_affected > 0:
                                    if tx_affected > 0 and budget_affected > 0:
                                        st.warning(
                                            f"{tx_affected} transactions and "
                                            f"{budget_affected} budgets will be affected "
                                            f"by deleting '{name}'."
                                        )
                                    elif tx_affected > 0:
                                        st.warning(
                                            f"{tx_affected} transactions will be affected "
                                            f"by deleting '{name}'."
                                        )
                                    else:
                                        # case đề bài: "This will also affect 2 budgets"
                                        st.warning(
                                            f"This will also affect {budget_affected} budgets."
                                        )

                                # Map label -> strategy code
                                if strategy_label.startswith("Block"):
                                    strategy = "block"
                                elif strategy_label.startswith("Reassign"):
                                    strategy = "reassign"
                                else:
                                    strategy = "cascade"

                                result = category_model.delete_category(
                                    category_type=item.get("type"),
                                    category_name=name,
                                    strategy=strategy,
                                )

                                if result.get("deleted"):
                                    st.success(
                                        "✅ "
                                        + result.get("message", "Category deleted.")
                                        + " ("
                                        f"{result.get('affected_transactions', 0)} transactions, "
                                        f"{result.get('affected_budgets', 0)} budgets affected)"
                                    )
                                    st.rerun()
                                else:
                                    st.error(result.get("message"))
    else:
        st.info("No categories yet.")


def _render_category_detail(category_model):
    st.subheader("Category detail")
    tab1, tab2 = st.tabs(config.TRANSACTION_TYPES)

    with tab1:
        _render_category_list(category_model, "Expense")

    with tab2:
        _render_category_list(category_model, "Income")

#TODO
def _render_add_category(category_model):
    st.subheader("Add category")
    with st.form("add_category_name"):
        col1, col2, col3 = st.columns([2, 2, 1]) # col1 and col2 is double size of col1

    # category type
    with col1:
        category_type = st.selectbox(
            "Category Type",
            config.TRANSACTION_TYPES # ["Expense", "Income"]
        )
    
    # category input
    with col2:
        category_name = st.text_input(
            "Category Name",
            placeholder="e.g., Groceries, Rent, Bonus"
        )
    
    with col3:
        st.write("")  # Spacing
        st.write("")
        submitted = st.form_submit_button("Submit", use_container_width=True)
    
    if submitted:
        if not category_name:
            st.error("❌ Please enter a category name")
        elif not category_type:
            st.error("❌ Please choose a category type")          
        else:
            result = category_model.upsert_category(category_type = category_type, category_name = category_name)
            if result:
                st.success(f"✅ Category '{category_name}' added successfully!")
                st.balloons()
                st.rerun()  # Refresh the page to show new category
            else:
                st.error("❌ Error adding category")


# public function
def render_categories(category_model):
    st.title("🏷️ Category Management")

    # Display existing category list
    _render_category_detail(category_model)

    st.divider()

    # Add category section
    _render_add_category(category_model)