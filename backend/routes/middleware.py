# backend/routes/middleware.py
# Authentication middleware - protects API routes

from functools import wraps
from flask import request, jsonify
from controllers.auth_controller import verify_token


def require_auth(f):
    """
    Decorator that checks for a valid Authorization header.
    Usage: @require_auth on any route function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token = None

        # Accept "Bearer <token>" format
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]

        if not verify_token(token):
            return jsonify({'error': 'Unauthorized. Please login.'}), 401

        return f(*args, **kwargs)
    return decorated
