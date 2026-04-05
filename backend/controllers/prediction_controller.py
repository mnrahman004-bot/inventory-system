# backend/controllers/prediction_controller.py
# AI prediction controller - bridges model data with ML module

from models.transaction_model import TransactionModel
from models.product_model import ProductModel
from ml.prediction import predict_demand


def get_prediction(product_id, days_ahead=30):
    """
    Fetch transaction history for a product and run ML prediction.
    Returns predicted demand and trend for the next N days.
    """
    # Validate product exists
    product = ProductModel.get_by_id(product_id)
    if not product:
        return {'error': 'Product not found'}, 404

    # Get transaction history
    transactions = TransactionModel.get_by_product(product_id)

    # Validate days_ahead parameter
    try:
        days_ahead = int(days_ahead)
        if days_ahead < 1 or days_ahead > 365:
            days_ahead = 30
    except (TypeError, ValueError):
        days_ahead = 30

    # Run prediction
    result = predict_demand(transactions, days_ahead=days_ahead)

    return {
        'product_id': product_id,
        'product_name': product['name'],
        'current_stock': product['quantity'],
        'prediction': result
    }, 200
