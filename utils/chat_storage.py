import json
import os
from datetime import datetime

CHAT_FILE = "data/chats.json"


def load_chats():

    if not os.path.exists(CHAT_FILE):
        return {}

    with open(CHAT_FILE, "r") as f:
        return json.load(f)


def save_chats(data):

    os.makedirs("data", exist_ok=True)

    with open(CHAT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_user_chats(username):

    data = load_chats()

    return data.get(username, [])


def create_chat(username):

    data = load_chats()

    user_chats = data.get(username, [])

    chat_id = str(datetime.now().timestamp())

    title = f"New Chat {datetime.now().strftime('%H:%M')}"

    chat = {
        "id": chat_id,
        "title": title,
        "messages": []
    }

    user_chats.append(chat)

    data[username] = user_chats

    save_chats(data)

    return chat_id


def add_message(username, chat_id, role, content):

    data = load_chats()

    for chat in data.get(username, []):

        if chat["id"] == chat_id:

            chat["messages"].append({
                "role": role,
                "content": content
            })

    save_chats(data)


def get_chat_messages(username, chat_id):

    chats = get_user_chats(username)

    for chat in chats:

        if chat["id"] == chat_id:
            return chat["messages"]

    return []


def delete_chat(username, chat_id):

    data = load_chats()

    chats = data.get(username, [])

    chats = [c for c in chats if c["id"] != chat_id]

    data[username] = chats

    save_chats(data)


def rename_chat(username, chat_id, new_title):

    data = load_chats()

    for chat in data.get(username, []):

        if chat["id"] == chat_id:
            chat["title"] = new_title

    save_chats(data)