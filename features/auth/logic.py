"""Password hashing and login validation using Google Sheets as user DB."""
import hashlib
import secrets
from data_layer.repository import load_users_from_sheet, save_user_to_sheet, delete_user_from_sheet


def hash_password(password: str) -> str:
    """Return pbkdf2$iterations$salt_hex$hash_hex"""
    salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
    return f"pbkdf2$100000${salt}${h}"


def verify_password(password: str, stored: str) -> bool:
    try:
        parts = stored.split("$")
        if parts[0] != "pbkdf2":
            return False
        iterations = int(parts[1])
        salt = parts[2]
        check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), iterations).hex()
        return check == parts[3]
    except (IndexError, ValueError):
        return False


def validate_login(username: str, password: str) -> dict | None:
    """Return user info dict if valid, None otherwise."""
    users = load_users_from_sheet()
    entry = users.get(username.strip())
    if entry is None:
        return None
    if verify_password(password.strip(), entry["password_hash"]):
        return {"username": username.strip(), "role": entry["role"], "centers": entry["centers"]}
    return None


def add_user(username: str, password: str, role: str, centers: str) -> bool:
    """Admin adds a new user or updates password."""
    h = hash_password(password)
    return save_user_to_sheet(username.strip(), h, role.strip(), centers.strip())


def remove_user(username: str) -> bool:
    return delete_user_from_sheet(username.strip())
