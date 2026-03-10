import json
import hashlib
from pathlib import Path
from auth.roles import USER, ADMIN

USERS_FILE = Path("storage/users.json")


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text())
    return {}


def save_users(users: dict):
    USERS_FILE.parent.mkdir(exist_ok=True)
    USERS_FILE.write_text(json.dumps(users, indent=2))


def register_user(username: str, password: str) -> bool:

    users = load_users()

    if username in users:
        return False

    users[username] = {
        "password": hash_password(password),
        "role": USER
    }

    save_users(users)
    return True


def login_user(username: str, password: str):

    users = load_users()

    if username not in users:
        return None

    hashed = hash_password(password)

    if users[username]["password"] != hashed:
        return None

    return users[username]["role"]