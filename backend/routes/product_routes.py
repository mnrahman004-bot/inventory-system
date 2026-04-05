# backend/routes/product_routes.py
# Product CRUD API routes

from flask import Blueprint, request, jsonify
from controllers.product_controller import (
    get_all_products, get_product, create_product,
    update_product, delete_product
)
from routes.middleware import require_auth

product_bp = Blueprint('products', __name__)


@product_bp.route('', methods=['GET'])
@require_auth
def list_products():
    """GET /api/products - List all products."""
    result, status = get_all_products()
    return jsonify(result), status


@product_bp.route('/<int:product_id>', methods=['GET'])
@require_auth
def get_one(product_id):
    """GET /api/products/<id> - Get a single product."""
    result, status = get_product(product_id)
    return jsonify(result), status


@product_bp.route('', methods=['POST'])
@require_auth
def create():
    """POST /api/products - Create a new product."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400
    result, status = create_product(data)
    return jsonify(result), status


@product_bp.route('/<int:product_id>', methods=['PUT'])
@require_auth
def update(product_id):
    """PUT /api/products/<id> - Update a product."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400
    result, status = update_product(product_id, data)
    return jsonify(result), status


@product_bp.route('/<int:product_id>', methods=['DELETE'])
@require_auth
def delete(product_id):
    """DELETE /api/products/<id> - Delete a product."""
    result, status = delete_product(product_id)
    return jsonify(result), status
