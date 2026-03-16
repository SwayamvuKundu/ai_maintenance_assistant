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

def stream_response(response, chunk_size=15):
    """
    Generator function to stream response text character by character.
    Yields chunks of text to create streaming effect.
    
    Args:
        response: Full response text from RAG
        chunk_size: Number of characters to yield at once (default 15 for smooth streaming)
    
    Yields:
        Chunks of response text
    """
    for i in range(0, len(response), chunk_size):
        yield response[i:i + chunk_size]