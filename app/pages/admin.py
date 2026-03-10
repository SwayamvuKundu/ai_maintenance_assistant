import streamlit as st

if st.session_state.get("role")!="admin":
    st.error("Access denied")
    st.stop()