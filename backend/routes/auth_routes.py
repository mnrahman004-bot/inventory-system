# backend/routes/auth_routes.py
# Authentication API routes

from flask import Blueprint, request, jsonify
from controllers.auth_controller import login, signup

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login_route():
    """POST /api/login - Authenticate user and return token."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400
    result, status = login(data.get('username'), data.get('password'))
    return jsonify(result), status


@auth_bp.route('/signup', methods=['POST'])
def signup_route():
    """POST /api/signup - Register a new user."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400
    result, status = signup(
        data.get('username'),
        data.get('password'),
        data.get('confirm_password')
    )
    return jsonify(result), status
