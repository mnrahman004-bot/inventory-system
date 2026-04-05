# backend/routes/prediction_routes.py
# AI prediction API routes

from flask import Blueprint, request, jsonify
from controllers.prediction_controller import get_prediction
from routes.middleware import require_auth

prediction_bp = Blueprint('predictions', __name__)


@prediction_bp.route('/<int:product_id>', methods=['GET'])
@require_auth
def predict(product_id):
    """GET /api/predict/<product_id>?days=30 - Get AI demand prediction."""
    days_ahead = request.args.get('days', 30)
    result, status = get_prediction(product_id, days_ahead)
    return jsonify(result), status
