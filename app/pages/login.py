import streamlit as st
from auth.auth_service import login_user
from utils.helpers import render_toast

render_toast()
st.title("🔐 Login to ForgeAI")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    role = login_user(username, password)

    if role:

        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = role

        if role == "admin":
            st.switch_page("pages/admin.py")
        else:
            st.switch_page("pages/chat.py")

    else:
        st.toast("Invalid username or password",icon="❌")

st.divider()

if st.button("🔙 Back to Home"):
    st.switch_page("pages/landing.py")