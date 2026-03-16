import streamlit as st
from utils.helpers import render_toast

st.set_page_config(page_title="ForgeAI", page_icon="🏭", layout="wide")
render_toast()

# Initialize session state for guest mode
if "guest_mode" not in st.session_state:
    st.session_state.guest_mode = False
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("🏭 ForgeAI")
st.subheader("AI-Powered Manufacturing Equipment Maintenance Assistant")

st.write("Get **instant, accurate answers** about equipment maintenance, troubleshooting, and repairs from intelligent analysis of manuals and maintenance documents.")

st.divider()

col1, col2, col3 = st.columns([1, 1, 1], gap="large")

with col1:
    st.markdown("### 💬 Guest Mode")
    st.write("Try ForgeAI without creating an account")
    if st.button("Start Chatting", key="guest", use_container_width=True, type="primary"):
        st.session_state.guest_mode = True
        st.session_state.logged_in = False
        st.session_state.username = "Guest"
        st.switch_page("pages/chat.py")
        
with col2:
    st.markdown("### 🔐 Login")
    st.write("Access your saved chat history")
    if st.button("Login", key="login", use_container_width=True, type="primary"):
        st.switch_page("pages/login.py")
        
with col3:
    st.markdown("### 📝 Register")
    st.write("Create an account to save chats")
    if st.button("Register", key="register", use_container_width=True, type="primary"):
        st.switch_page("pages/register.py")

st.divider()
st.markdown("## Why ForgeAI?")

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("**📕 Instant Access**")
    st.write("Query equipment manuals without manual searching")
    
with f2:
    st.markdown("**🛠️ Fast Troubleshooting**")
    st.write("Identify issues and corrective actions instantly")
    
with f3:
    st.markdown("**🤖 Context-Aware**")
    st.write("Natural conversations with multi-turn context")

st.divider()

st.markdown("## For Everyone")

r1, r2 = st.columns(2)

with r1:
    st.markdown("**🧑‍🏭 Maintenance Staff**")
    st.write("""
    - Ask questions naturally
    - Get step-by-step guidance
    - View saved conversations
    - No technical knowledge needed
    """)
    
with r2:
    st.markdown("**👨‍💼 Administrators**")
    st.write("""
    - Upload equipment manuals
    - Manage knowledge base
    - Rebuild AI index
    - Keep documentation current
    """)

st.divider()

st.caption("ForgeAI - Manufacturing Excellence | All rights reserved")
