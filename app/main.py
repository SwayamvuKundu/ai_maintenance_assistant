import streamlit as st

# Initialize session state for authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

if "current_page" not in st.session_state:
    st.session_state.current_page = None

# If user is logged in, redirect to their last page
if st.session_state.logged_in:
    if st.session_state.role == "admin":
        st.switch_page("pages/admin.py")
    else:
        st.switch_page("pages/chat.py")
else:
    # Route to landing page
    st.switch_page("pages/landing.py")
