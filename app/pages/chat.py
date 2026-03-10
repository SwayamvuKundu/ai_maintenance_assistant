import streamlit as st
from utils.chat_storage import (
    get_user_chats,
    create_chat,
    add_message,
    get_chat_messages,
    delete_chat,
    rename_chat
)
from datetime import datetime

st.set_page_config(page_title="Maintenance AI", layout="wide")

# -------------------------
# USER
# -------------------------

username = st.session_state.get("user")

guest_mode = username is None

if guest_mode:
    username = "guest"

# -------------------------
# SESSION STATE
# -------------------------

if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

# -------------------------
# SIDEBAR
# -------------------------

with st.sidebar:

    st.title("Maintenance AI")

    if not guest_mode:

        if st.button("➕ New Chat"):

            new_chat_id = create_chat(username)

            st.session_state.chat_id = new_chat_id

            st.rerun()

        chats = get_user_chats(username)

        st.divider()

        for chat in chats:

            col1, col2, col3 = st.columns([6,1,1])

            with col1:

                if st.button(
                    chat["title"][:30],
                    key=f"chat_{chat['id']}"
                ):

                    st.session_state.chat_id = chat["id"]

                    st.rerun()

            with col2:

                with st.popover("✏️"):

                    new_title = st.text_input(
                        "Rename chat",
                        value=chat["title"],
                        key=f"rename_{chat['id']}"
                    )

                    if st.button(
                        "Save",
                        key=f"save_{chat['id']}"
                    ):

                        rename_chat(
                            username,
                            chat["id"],
                            new_title
                        )

                        st.toast("Renamed")

                        st.rerun()

            with col3:

                if st.button(
                    "🗑",
                    key=f"del_{chat['id']}"
                ):

                    delete_chat(
                        username,
                        chat["id"]
                    )

                    st.toast("Chat deleted")

                    st.rerun()

    else:

        st.info("Guest mode (no chat history)")

# -------------------------
# MAIN CHAT AREA
# -------------------------

st.title("Manufacturing Maintenance Assistant")

# -------------------------
# LOAD MESSAGES
# -------------------------

messages = []

if not guest_mode and st.session_state.chat_id:

    messages = get_chat_messages(
        username,
        st.session_state.chat_id
    )

for msg in messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# USER INPUT
# -------------------------

prompt = st.chat_input("Ask about equipment maintenance...")

if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)

    if not guest_mode and st.session_state.chat_id:

        add_message(
            username,
            st.session_state.chat_id,
            "user",
            prompt
        )

    # Dummy AI response for now
    response = f"AI Response for: {prompt}"

    with st.chat_message("assistant"):
        st.markdown(response)

    if not guest_mode and st.session_state.chat_id:

        add_message(
            username,
            st.session_state.chat_id,
            "assistant",
            response
        )