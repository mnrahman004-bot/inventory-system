# backend/app.py
# Flask application entry point - registers all blueprints and starts the server

import os
from flask import Flask, jsonify
from flask_cors import CORS

from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.transaction_routes import transaction_bp
from routes.report_routes import report_bp
from routes.prediction_routes import prediction_bp


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)

    # Enable CORS for all origins (restrict in production)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register all API blueprints under /api prefix
    app.register_blueprint(auth_bp,        url_prefix='/api')
    app.register_blueprint(product_bp,     url_prefix='/api/products')
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
    app.register_blueprint(report_bp,      url_prefix='/api/reports')
    app.register_blueprint(prediction_bp,  url_prefix='/api/predict')

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok', 'message': 'Inventory API is running'}), 200

    # 404 handler
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Endpoint not found'}), 404

    # 500 handler
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error'}), 500

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
