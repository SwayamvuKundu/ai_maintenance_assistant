import streamlit as st

def show_toast(message, icon="✅"):
    st.toast(message, icon=icon)


def flash_toast(message, icon="✅"):
    st.session_state.toast_message = message
    st.session_state.toast_icon = icon


def render_toast():
    if "toast_message" in st.session_state:
        st.toast(
            st.session_state.toast_message,
            icon=st.session_state.get("toast_icon", "✅")
        )
        del st.session_state.toast_message
        del st.session_state.toast_icon