# backend/controllers/transaction_controller.py
# Business logic for stock transactions (IN/OUT)

from models.transaction_model import TransactionModel
from models.product_model import ProductModel


def get_all_transactions():
    """Return all transactions with product names."""
    transactions = TransactionModel.get_all()
    for t in transactions:
        if t.get('date'):
            t['date'] = str(t['date'])
    return {'transactions': transactions}, 200


def create_transaction(data):
    """
    Process a stock transaction.
    - 'IN' increases stock quantity
    - 'OUT' decreases stock quantity (prevents negative stock)
    """
    product_id = data.get('product_id')
    tx_type = data.get('type', '').upper()
    quantity = data.get('quantity')

    # Validation
    if not product_id:
        return {'error': 'Product ID is required'}, 400
    if tx_type not in ('IN', 'OUT'):
        return {'error': 'Transaction type must be IN or OUT'}, 400
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError()
    except (TypeError, ValueError):
        return {'error': 'Quantity must be a positive integer'}, 400

    # Check product exists
    product = ProductModel.get_by_id(product_id)
    if not product:
        return {'error': 'Product not found'}, 404

    # Calculate stock delta
    delta = quantity if tx_type == 'IN' else -quantity

    # Prevent negative stock for OUT transactions
    if tx_type == 'OUT' and product['quantity'] < quantity:
        return {
            'error': f'Insufficient stock. Available: {product["quantity"]}, Requested: {quantity}'
        }, 400

    # Update product quantity
    success = ProductModel.update_quantity(product_id, delta)
    if not success:
        return {'error': 'Failed to update stock quantity'}, 500

    # Record the transaction
    tx_id = TransactionModel.create(product_id, tx_type, quantity)
    if tx_id is None:
        return {'error': 'Failed to record transaction'}, 500

    return {
        'message': f'Stock {"added" if tx_type == "IN" else "removed"} successfully',
        'transaction_id': tx_id,
        'new_quantity': product['quantity'] + delta
    }, 201


def get_sales_vs_purchases():
    """Return sales vs purchases data for dashboard charts."""
    data = TransactionModel.get_recent_sales_vs_purchases(days=30)
    for row in data:
        row['day'] = str(row['day'])
    return {'data': data}, 200
