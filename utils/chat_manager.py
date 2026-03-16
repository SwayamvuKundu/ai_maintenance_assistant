import json
import uuid
from pathlib import Path
from datetime import datetime

STORAGE_DIR = Path("storage/chat")

def get_user_chat_dir(username: str) -> Path:
    """Get or create user's chat directory"""
    user_dir = STORAGE_DIR / username
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir

def create_new_chat(username: str) -> dict:
    """Create a new chat with UUID and timestamp"""
    user_dir = get_user_chat_dir(username)
    chat_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%b %d, %H:%M")
    chat_name = f"Chat - {timestamp}"
    
    chat_data = {
        "id": chat_id,
        "name": chat_name,
        "created_at": datetime.now().isoformat(),
        "messages": []
    }
    
    chat_file = user_dir / f"{chat_id}.json"
    chat_file.write_text(json.dumps(chat_data, indent=2))
    
    return chat_data

def get_user_chats(username: str) -> list:
    """Get all chats for a user, sorted by creation time"""
    user_dir = get_user_chat_dir(username)
    chats = []
    
    for chat_file in user_dir.glob("*.json"):
        chat_data = json.loads(chat_file.read_text())
        chats.append(chat_data)
    
    return sorted(chats, key=lambda x: x["created_at"], reverse=True)

def load_chat(username: str, chat_id: str) -> dict:
    """Load a specific chat"""
    user_dir = get_user_chat_dir(username)
    chat_file = user_dir / f"{chat_id}.json"
    
    if chat_file.exists():
        return json.loads(chat_file.read_text())
    return None

def save_chat(username: str, chat_data: dict) -> bool:
    """Save chat data"""
    user_dir = get_user_chat_dir(username)
    chat_file = user_dir / f"{chat_data['id']}.json"
    
    try:
        chat_file.write_text(json.dumps(chat_data, indent=2))
        return True
    except Exception as e:
        print(f"[v0] Error saving chat: {e}")
        return False

def rename_chat(username: str, chat_id: str, new_name: str) -> bool:
    """Rename a chat"""
    chat_data = load_chat(username, chat_id)
    
    if not chat_data:
        return False
    
    chat_data["name"] = new_name
    return save_chat(username, chat_data)

def delete_chat(username: str, chat_id: str) -> bool:
    """Delete a chat"""
    user_dir = get_user_chat_dir(username)
    chat_file = user_dir / f"{chat_id}.json"
    
    try:
        if chat_file.exists():
            chat_file.unlink()
        return True
    except Exception as e:
        print(f"[v0] Error deleting chat: {e}")
        return False
