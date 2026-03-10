import streamlit as st

from utils.helpers import render_toast

render_toast()
st.set_page_config(
    page_title="ForgeAI",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 ForgeAI")
st.subheader("AI-Powered Manufacturing Maintenance Assistant")

st.write(
"""
Get **instant, accurate answers** from equipment manuals,
troubleshooting guides, and maintenance documents.
"""
)

st.write("")

col1, col2, col3 = st.columns(3)


with col1:
    st.success("💬 Try Without Login")

    if st.button("Start Chatting", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.username = "guest"
        st.session_state.role = "guest"

        st.switch_page("pages/chat.py")


with col2:
    st.info("🔐 Existing User")

    if st.button("Login", use_container_width=True):
        st.switch_page("pages/login.py")


with col3:
    st.warning("📝 New User")

    if st.button("Register", use_container_width=True):
        st.switch_page("pages/register.py")

st.divider()

st.header("🚀 Why ForgeAI?")

f1, f2, f3 = st.columns(3)

with f1:
    st.metric("📕 Manuals", "Instant Access")
    st.write(
        "Query large equipment manuals and maintenance documents "
        "without searching PDFs manually."
    )

with f2:
    st.metric("🛠️ Troubleshooting", "Faster Repairs")
    st.write(
        "Identify causes, symptoms, and corrective actions "
        "for industrial failures."
    )

with f3:
    st.metric("🤖 AI-Driven", "Context Aware")
    st.write(
        "Understands follow-up questions and maintains "
        "conversation context like a real assistant."
    )

st.divider()

st.caption("ForgeAI • Built for manufacturing excellence")