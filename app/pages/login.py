import streamlit as st
from auth.auth_service import login_user
from utils.helpers import show_toast, render_toast, flash_toast

st.set_page_config(page_title="Login - ForgeAI", page_icon="🔐", layout="centered")

# Render any pending toasts
render_toast()

# Add some vertical spacing
st.write("")
st.write("")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.title("🔐 ForgeAI Login")
    st.markdown("Enter your credentials to access the maintenance assistant")
    
    st.divider()
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        
        submit = st.form_submit_button("Login", use_container_width=True, type="primary")
    
    if submit:
        if not username or not password:
            show_toast("Please enter both username and password", icon="❌")
        else:
            role = login_user(username, password)
            
            if role:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = role
                flash_toast(f"Welcome back, {username}!", icon="✅")
                
                if role == "admin":
                    st.switch_page("pages/admin.py")
                else:
                    st.switch_page("pages/chat.py")
            else:
                show_toast("Invalid username or password", icon="❌")
    
    st.divider()
    
    st.write("Don't have an account?")
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("Register here", use_container_width=True):
            st.switch_page("pages/register.py")
    
    with col_b:
        if st.button("Back to Home", use_container_width=True):
            st.switch_page("pages/landing.py")
