import streamlit as st
from auth.auth_service import register_user
from utils.helpers import render_toast,flash_toast

render_toast()
st.title("📝 Register for ForgeAI")

username = st.text_input("Choose a username")
password = st.text_input("Choose a password", type="password")
confirm = st.text_input("Confirm password", type="password")

if st.button("Register"):

    if not username or not password:
        st.error("Please fill all fields")

    elif password != confirm:
        st.error("Passwords do not match")

    else:

        success = register_user(username, password)

        if success:
            flash_toast("Registration successful! Please login.", "🎉")
            st.switch_page("pages/login.py")

        else:
            st.toast("Username already exists",icon="❌")

st.divider()

if st.button("🔙 Back to Home"):
    st.switch_page("pages/landing.py")