from database.user_model import UserModel
import streamlit as st
import time
from typing import Any, Optional 

def render_user_profile(user_model: UserModel, user: dict[str, any]):
    
    if 'user_settings_open' not in st.session_state:
        st.session_state['user_settings_open'] = False

    # Create a more compact profile container
    with st.sidebar:
        st.divider()
        
        col1, col2, col3 = st.columns([0.8, 3.2, 0.8], gap="small")
        
        with col1:
            avatar_url = user.get("picture")
            if avatar_url:
                st.image(avatar_url, width=40)
            else:
                st.write("👤")
        
        with col2:
            if st.button("❌ Deactivate", use_container_width=True, key="deactivate_button_settings"):
                user_id = user.get("id")

                if user_id:
                    user_model.deactivate_user(user_id)
                    st.success("Account deactivated. Goodbye!")
                    time.sleep(1)
                    st.logout()
                    st.rerun()
                else:
                    st.error("Unable to determine user id.")

            st.write("")  
            with st.expander("🧨 Delete account & all data", expanded=False):
                st.markdown(
                    "**⚠️ This will permanently delete all your data.**"
                )
                confirm = st.checkbox(
                    "I understand and want to permanently delete my account.",
                    key="confirm_delete_account",
                )

                if st.button(
                    "🗑️ Delete my account permanently",
                    use_container_width=True,
                    key="delete_account_button",
                ):
                    if not confirm:
                        st.error("Please confirm before deleting your account.")
                    elif user_id:
                        summary = user_model.delete_user_with_data(user_id)
                        st.success(summary.get("message", "Account deleted."))
                        time.sleep(1)
                        st.logout()
                        st.rerun()
                    else:
                        st.error("Unable to determine user id.")

        st.caption("_Account settings_")
        
        with col3:
            if st.button("⚙️", key="settings_toggle", help="Settings"):
                st.session_state['user_settings_open'] = not st.session_state['user_settings_open']
        
    if st.session_state['user_settings_open']: # is True
        _render_user_settings(user_model, user.get("id"))
        st.divider()


def _render_user_settings(user_model, user_id: str):
    st.markdown("**⚙️ Settings**")
    
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        if st.button("🚪 Log out", use_container_width=True, key="logout_button_settings"):
            st.logout()
    
    with col2:
        if st.button("❌ Deactivate", use_container_width=True, key="deactivate_button"):
            if user_id:
                user_model.deactivate_user(user_id)
                st.success("Account deactivated. Goodbye!")
                time.sleep(1)
                st.logout()
                st.rerun()
            else:
                st.error("Unable to determine user id.")
    
        st.write("")

            # 🔥 Delete account & all data
        with st.expander("🧨 Delete account & all data", expanded=False):
            st.markdown("**⚠️ This will permanently delete all your data.**")
            confirm = st.checkbox(
                "I understand and want to permanently delete my account.",
                key="confirm_delete_account_settings",
            )

            if st.button(
                "🗑️ Delete my account permanently",
                use_container_width=True,
                key="delete_account_button_settings",
            ):
                if not confirm:
                    st.error("Please confirm before deleting your account.")
                elif user_id:
                    summary = user_model.delete_user_with_data(user_id)
                    st.success(summary.get("message", "Account deleted."))
                    time.sleep(1)
                    st.logout()
                    st.rerun()
                else:
                    st.error("Unable to determine user id.")

    st.caption("_Account settings_")