# backend/controllers/auth_controller.py
# Handles login and signup logic

import bcrypt
import os
import hashlib
import re
from models.user_model import UserModel


def login(username, password):
    """
    Validate username + password.
    Returns a simple token on success.
    """
    if not username or not password:
        return {'error': 'Username and password required'}, 400

    user = UserModel.find_by_username(username)
    if not user:
        return {'error': 'Invalid credentials'}, 401

    # Verify bcrypt password
    try:
        password_bytes = password.encode('utf-8')
        stored_hash = user['password_hash'].encode('utf-8')
        if not bcrypt.checkpw(password_bytes, stored_hash):
            return {'error': 'Invalid credentials'}, 401
    except Exception as e:
        print(f"[AuthController] bcrypt error: {e}")
        return {'error': 'Authentication error'}, 500

    # Generate a simple deterministic token (for demo; use JWT in production)
    secret = os.getenv('SECRET_KEY', 'inventory_secret_2024')
    token_raw = f"{user['id']}:{user['username']}:{secret}"
    token = hashlib.sha256(token_raw.encode()).hexdigest()

    return {
        'token': token,
        'username': user['username'],
        'user_id': user['id']
    }, 200


def signup(username, password, confirm_password):
    """
    Register a new user account.
    Validates input, checks for duplicate username, hashes password.
    """
    if not username or not password or not confirm_password:
        return {'error': 'All fields are required'}, 400

    username = username.strip()

    # Username rules: 3–30 chars, alphanumeric + underscores
    if not re.match(r'^[a-zA-Z0-9_]{3,30}$', username):
        return {'error': 'Username must be 3–30 characters (letters, numbers, underscores only)'}, 400

    if len(password) < 6:
        return {'error': 'Password must be at least 6 characters'}, 400

    if password != confirm_password:
        return {'error': 'Passwords do not match'}, 400

    # Check if username already taken
    existing = UserModel.find_by_username(username)
    if existing:
        return {'error': 'Username already taken'}, 409

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    success = UserModel.create_user(username, password_hash)
    if not success:
        return {'error': 'Failed to create account'}, 500

    return {'message': 'Account created successfully'}, 201


def verify_token(token):
    """
    Simple token verification.
    In production, replace with JWT validation.
    """
    if not token:
        return False
    # For demo purposes, accept any non-empty token
    # In production: decode JWT and validate expiry
    return len(token) == 64  # SHA-256 hex = 64 chars
