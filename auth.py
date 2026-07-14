import bcrypt
import re
from database import get_user_by_username, add_user

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a password against its bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validates the password strength.
    Requires at least 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, "Strong password."

def register_user(fullname, email, phone, hospital, role, username, password, confirm_password, agree_terms):
    """Registers a new user after validations."""
    if not fullname or not email or not phone or not hospital or not role or not username or not password:
        return False, "All fields are required."
    
    if password != confirm_password:
        return False, "Passwords do not match."
        
    if not agree_terms:
        return False, "You must agree to the Terms and Conditions."
        
    # Email simple validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email address format."
        
    # Password strength check
    is_strong, msg = validate_password_strength(password)
    if not is_strong:
        return False, msg
        
    # Hash password and insert
    hashed_pwd = hash_password(password)
    success, db_msg = add_user(fullname, email, phone, hospital, role, username, hashed_pwd)
    return success, db_msg

def authenticate_user(username, password):
    """Authenticates a user by username and password."""
    user = get_user_by_username(username)
    if not user:
        return False, "Invalid username or password.", None
        
    if verify_password(password, user["password"]):
        return True, "Authentication successful.", user
        
    return False, "Invalid username or password.", None
