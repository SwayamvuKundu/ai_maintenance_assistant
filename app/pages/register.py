import streamlit as st
from auth.auth_service import register_user
from utils.helpers import show_toast, flash_toast, render_toast

st.set_page_config(page_title="Register - ForgeAI", page_icon="📝", layout="centered")

# Render any pending toasts
render_toast()

st.write("")
st.write("")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.title("📝 Create Account")
    st.markdown("Join ForgeAI to save your maintenance conversations")
    
    st.divider()
    
    with st.form("register_form"):
        username = st.text_input("Username", placeholder="Choose a unique username")
        password = st.text_input("Password", placeholder="Minimum 4 characters", type="password")
        confirm = st.text_input("Confirm Password", placeholder="Re-enter your password", type="password")
        
        submit = st.form_submit_button("Register", use_container_width=True, type="primary")
    
    if submit:
        if not username or not password or not confirm:
            show_toast("Please fill in all fields", icon="❌")
        elif len(password) < 4:
            show_toast("Password must be at least 4 characters", icon="❌")
        elif password != confirm:
            show_toast("Passwords do not match", icon="❌")
        else:
            success = register_user(username, password)
            if success:
                flash_toast("Registration successful! Redirecting to login...", icon="✅")
                st.switch_page("pages/login.py")
            else:
                show_toast("Username already exists. Please choose another.", icon="❌")
    
    st.divider()
    
    st.write("Already have an account?")
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("Login here", use_container_width=True):
            st.switch_page("pages/login.py")
    
    with col_b:
        if st.button("Back to Home", use_container_width=True):
            st.switch_page("pages/landing.py")
