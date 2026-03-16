import streamlit as st
import shutil
from pathlib import Path
from memory.conversation import add_to_memory
from rag.chains import run_rag
from utils.helpers import show_toast, render_toast, stream_response, flash_toast

st.set_page_config(page_title="Admin - ForgeAI", page_icon="⚙️", layout="wide")

render_toast()

if st.session_state.get("role") != "admin":
    show_toast("Access denied. Admin only.", icon="❌")
    st.stop()

if "admin_chat" not in st.session_state:
    st.session_state.admin_chat = []
if "admin_memory" not in st.session_state:
    st.session_state.admin_memory = []

with st.sidebar:
    st.title("Admin Panel")
    st.caption("ForgeAI Management")
    st.divider()
    
    if st.button("Home", use_container_width=True):
        st.switch_page("pages/landing.py")
    
    if st.button("Logout", use_container_width=True, type="secondary"):
        flash_toast("Logged out successfully", icon="👋")
        st.session_state.clear()
        st.switch_page("pages/landing.py")

st.title("Admin Dashboard")
st.caption(f"Logged in as: {st.session_state.get('username', 'Admin')}")

tab1, tab2, tab3 = st.tabs(["Chat", "Knowledge Base", "System"])

with tab1:
    st.subheader("Admin Chat & Testing")
    
    for msg in st.session_state.admin_chat:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("Test a query..."):
        st.session_state.admin_chat.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Analyzing query..."):
                try:
                    response, sources = run_rag(prompt, st.session_state.admin_memory)
                except:
                    response = "Unable to retrieve information. Knowledge base may be empty."
                st.session_state.admin_memory = add_to_memory(st.session_state.admin_memory, prompt, response)
                st.write_stream(stream_response(response, chunk_size=15))
        
        st.session_state.admin_chat.append({"role": "assistant", "content": response})

with tab2:
    st.subheader("Knowledge Base Management")
    
    manuals_dir = Path("data/manuals")
    logs_dir = Path("data/logs")
    processed_dir = Path("data/processed")
    
    manual_count = len(list(manuals_dir.glob("*"))) if manuals_dir.exists() else 0
    logs_count = len(list(logs_dir.glob("*"))) if logs_dir.exists() else 0
    processed_count = len(list(processed_dir.glob("*"))) if processed_dir.exists() else 0
    total_docs = manual_count + logs_count + processed_count
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Documents", total_docs)
        st.metric("PDF Manuals", manual_count)
    with col2:
        st.metric("JSON Logs", logs_count)
        st.metric("CSV Processed", processed_count)
    
    st.divider()
    st.write("**Existing Documents**")
    
    if total_docs > 0:
        col_manuals, col_logs, col_processed = st.columns(3)
        
        with col_manuals:
            if manual_count > 0:
                st.write(f"**PDF Manuals ({manual_count})**")
                for doc in manuals_dir.glob("*"):
                    col_name, col_del = st.columns([4, 1])
                    with col_name:
                        st.caption(doc.name)
                    with col_del:
                        if st.button("🗑️", key=f"del_manual_{doc.name}", help="Delete"):
                            doc.unlink()
                            flash_toast(f"Deleted: {doc.name}", icon="🗑️")
                            st.rerun()
        
        with col_logs:
            if logs_count > 0:
                st.write(f"**JSON Logs ({logs_count})**")
                for doc in logs_dir.glob("*"):
                    col_name, col_del = st.columns([4, 1])
                    with col_name:
                        st.caption(doc.name)
                    with col_del:
                        if st.button("🗑️", key=f"del_log_{doc.name}", help="Delete"):
                            doc.unlink()
                            flash_toast(f"Deleted: {doc.name}", icon="🗑️")
                            st.rerun()
        
        with col_processed:
            if processed_count > 0:
                st.write(f"**CSV Processed ({processed_count})**")
                for doc in processed_dir.glob("*"):
                    col_name, col_del = st.columns([4, 1])
                    with col_name:
                        st.caption(doc.name)
                    with col_del:
                        if st.button("🗑️", key=f"del_processed_{doc.name}", help="Delete"):
                            doc.unlink()
                            flash_toast(f"Deleted: {doc.name}", icon="🗑️")
                            st.rerun()
    else:
        st.info("No documents uploaded yet. Upload your first document below.")
    
    st.divider()
    st.write("**Upload Documents**")
    st.caption("Upload multiple files at once. PDFs go to Manuals, JSONs to Logs, CSVs to Processed.")
    
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "csv", "json"], accept_multiple_files=True)
    
    if uploaded_files and st.button("Upload Documents", use_container_width=True, type="primary"):
        for uploaded_file in uploaded_files:
            file_ext = Path(uploaded_file.name).suffix.lower()
            
            if file_ext == ".pdf":
                upload_dir = Path("data/manuals")
            elif file_ext == ".json":
                upload_dir = Path("data/logs")
            elif file_ext == ".csv":
                upload_dir = Path("data/processed")
            else:
                continue
            
            upload_dir.mkdir(parents=True, exist_ok=True)
            file_path = upload_dir / uploaded_file.name
            file_path.write_bytes(uploaded_file.getbuffer())
            flash_toast(f"Uploaded: {uploaded_file.name}", icon="📁")
        
        st.rerun()
    
    st.divider()
    st.write("**Rebuild Knowledge Base**")
    st.caption("Deletes and rebuilds the vector store from all documents.")
    
    if st.button("Rebuild Vector Store", use_container_width=True, type="primary"):
        with st.spinner("Rebuilding vector store..."):
            try:
                vectorstore_path = Path("vectorstore/db")
                if vectorstore_path.exists():
                    shutil.rmtree(vectorstore_path)
                
                from embeddings.build_vectorstore import build_vectorstore
                build_vectorstore()
                show_toast("Vector store rebuilt successfully!", icon="✅")
                st.balloons()
            except Exception as e:
                show_toast(f"Error: {str(e)}", icon="❌")

with tab3:
    st.subheader("System Configuration")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Status", "Active")
    with col2:
        st.metric("Vector DB", "Chroma")
    with col3:
        st.metric("Embedding Model", "MiniLM-L6")
    
    st.divider()
    st.write("**Configuration Settings**")
    config_info = """
    - **Chunk Size**: 600 characters
    - **Chunk Overlap**: 100 characters
    - **Top K Retrieval**: 8 documents
    - **Fetch K**: 18 documents
    - **Lambda Multiplier**: 0.7 (for MMR)
    - **Vector DB**: Chroma (Local)
    - **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
    - **LLM**: Google Gemini Flash
    """
    st.write(config_info)
