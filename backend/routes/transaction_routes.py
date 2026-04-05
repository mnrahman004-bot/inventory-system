# backend/routes/transaction_routes.py
# Transaction API routes

from flask import Blueprint, request, jsonify
from controllers.transaction_controller import (
    get_all_transactions, create_transaction, get_sales_vs_purchases
)
from routes.middleware import require_auth

transaction_bp = Blueprint('transactions', __name__)


@transaction_bp.route('', methods=['GET'])
@require_auth
def list_transactions():
    """GET /api/transactions - List all transactions."""
    result, status = get_all_transactions()
    return jsonify(result), status


@transaction_bp.route('', methods=['POST'])
@require_auth
def create():
    """POST /api/transactions - Create a new stock transaction."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400
    result, status = create_transaction(data)
    return jsonify(result), status


@transaction_bp.route('/chart', methods=['GET'])
@require_auth
def chart_data():
    """GET /api/transactions/chart - Sales vs purchases for chart."""
    result, status = get_sales_vs_purchases()
    return jsonify(result), status
