import streamlit as st
from memory.conversation import add_to_memory
from rag.chains import run_rag
from utils.chat_manager import create_new_chat, get_user_chats, load_chat, save_chat, rename_chat, delete_chat
from utils.helpers import show_toast, render_toast, stream_response, flash_toast

st.set_page_config(page_title="Chat - ForgeAI", page_icon="💬", layout="wide")

# Render any pending toasts
render_toast()

# Initialize session state - don't override if already logged in
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "memory" not in st.session_state:
    st.session_state.memory = []

if "rename_mode" not in st.session_state:
    st.session_state.rename_mode = None

if "chat_menu" not in st.session_state:
    st.session_state.chat_menu = None

# Set guest mode only if not logged in
if not st.session_state.get("logged_in"):
    st.session_state.guest_mode = True
    # Clear any previous guest messages when entering guest mode (for first time)
    if st.session_state.get("was_logged_in"):
        st.session_state.chat_messages = []
        st.session_state.memory = []
    st.session_state.was_logged_in = False
else:
    # User just logged in - clear guest messages and mark as logged in
    if not st.session_state.get("was_logged_in"):
        st.session_state.chat_messages = []
        st.session_state.memory = []
        st.session_state.current_chat_id = None
    st.session_state.was_logged_in = True
    st.session_state.guest_mode = False

# Sidebar with chat history
with st.sidebar:
    st.title("ForgeAI")
    st.caption("Manufacturing Maintenance Assistant")
    
    if st.button("New Chat", use_container_width=True, type="primary"):
        if st.session_state.get("logged_in"):
            new_chat = create_new_chat(st.session_state.username)
            st.session_state.current_chat_id = new_chat["id"]
            st.session_state.chat_messages = []
            st.session_state.memory = []
            flash_toast("New chat created", icon="✨")
        else:
            st.session_state.chat_messages = []
            st.session_state.memory = []
        st.rerun()
    
    st.divider()
    
    # Chat history for logged-in users
    if st.session_state.get("logged_in"):
        st.write("**Chat History**")
        user_chats = get_user_chats(st.session_state.username)
        
        if user_chats:
            for chat in user_chats:
                # Highlight current chat
                is_current = chat["id"] == st.session_state.current_chat_id
                
                col_chat, col_options = st.columns([4, 1])
                
                with col_chat:
                    # Show inline rename input if in rename mode for this chat
                    if st.session_state.get("rename_mode") == chat["id"]:
                        new_name = st.text_input(
                            "Rename chat",
                            value=chat["name"],
                            key=f"rename_input_{chat['id']}",
                            label_visibility="collapsed"
                        )
                        # Auto-save on Enter (Streamlit behavior)
                        if new_name and new_name != chat["name"]:
                            rename_chat(st.session_state.username, chat["id"], new_name)
                            flash_toast(f"Chat renamed to '{new_name}'", icon="✏️")
                            st.session_state.rename_mode = None
                            st.rerun()
                    else:
                        if st.button(
                            f"{'→ ' if is_current else ''}{chat['name']}",
                            key=chat["id"],
                            use_container_width=True,
                            type="primary" if is_current else "secondary"
                        ):
                            st.session_state.current_chat_id = chat["id"]
                            chat_data = load_chat(st.session_state.username, chat["id"])
                            st.session_state.chat_messages = chat_data.get("messages", [])
                            
                            # Load last 5 message pairs (user + assistant) into memory
                            from memory.conversation import add_to_memory
                            st.session_state.memory = []
                            messages = chat_data.get("messages", [])
                            # Extract user-assistant pairs from messages
                            i = 0
                            while i < len(messages):
                                if i < len(messages) and messages[i].get("role") == "user":
                                    user_msg = messages[i].get("content", "")
                                    assistant_msg = ""
                                    if i + 1 < len(messages) and messages[i + 1].get("role") == "assistant":
                                        assistant_msg = messages[i + 1].get("content", "")
                                        i += 2
                                    else:
                                        i += 1
                                    st.session_state.memory = add_to_memory(st.session_state.memory, user_msg, assistant_msg)
                                else:
                                    i += 1
                            
                            st.rerun()
                
                with col_options:
                    if not st.session_state.get("rename_mode") == chat["id"]:
                        if st.button("⋮", key=f"menu_{chat['id']}", help="More options"):
                            st.session_state.chat_menu = chat["id"]
                
                # Show options if menu is open
                if st.session_state.get("chat_menu") == chat["id"]:
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        if st.button("✏️ Rename", key=f"rename_{chat['id']}", use_container_width=True):
                            st.session_state.rename_mode = chat["id"]
                            st.session_state.chat_menu = None
                            st.rerun()
                    
                    with col_b:
                        if st.button("🗑️ Delete", key=f"delete_{chat['id']}", use_container_width=True):
                            delete_chat(st.session_state.username, chat["id"])
                            if st.session_state.current_chat_id == chat["id"]:
                                st.session_state.current_chat_id = None
                                st.session_state.chat_messages = []
                            st.session_state.chat_menu = None
                            flash_toast("Chat deleted", icon="🗑️")
                            st.rerun()
        else:
            st.caption("No chats yet. Start a new conversation!")
    else:
        st.info("Guest Mode - Chats are not saved")
    
    st.divider()
    
    st.caption(f"User: {'👤 ' + st.session_state.username if st.session_state.get('logged_in') else '👁️ Guest'}")
    
    if st.session_state.get("logged_in"):
        if st.button("Logout", use_container_width=True):
            show_toast("Logged out successfully", icon="👋")
            st.session_state.clear()
            st.switch_page("pages/landing.py")
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", use_container_width=True):
                st.switch_page("pages/login.py")
        with col2:
            if st.button("Register", use_container_width=True):
                st.switch_page("pages/register.py")
    
    if st.button("Home", use_container_width=True):
        st.switch_page("pages/landing.py")

# Main chat area
st.title("Equipment Maintenance Assistant")

if not st.session_state.get("logged_in"):
    st.warning("Guest Mode - Your chats are not saved. Login to save conversations.")

# Display chat messages
for message in st.session_state.chat_messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about equipment maintenance..."):
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    st.session_state.chat_messages.append({
        "role": "user",
        "content": prompt
    })
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing your query..."):
            try:
                response, sources = run_rag(prompt, st.session_state.memory)
            except:
                response = "Unable to retrieve information. Please ensure the knowledge base is populated with equipment manuals."
            st.session_state.memory = add_to_memory(st.session_state.memory, prompt, response)
            st.write_stream(stream_response(response, chunk_size=15))
    
    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": response
    })
    
    # Save chat if logged in
    if st.session_state.get("logged_in"):
        is_new_chat = not st.session_state.current_chat_id
        
        if is_new_chat:
            new_chat = create_new_chat(st.session_state.username)
            st.session_state.current_chat_id = new_chat["id"]
        
        chat_data = load_chat(st.session_state.username, st.session_state.current_chat_id)
        chat_data["messages"] = st.session_state.chat_messages
        save_chat(st.session_state.username, chat_data)
        
        # Rerun only when a new chat is created to refresh sidebar
        if is_new_chat:
            st.rerun()