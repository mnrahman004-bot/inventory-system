# backend/routes/report_routes.py
# Report and dashboard API routes

from flask import Blueprint, request, jsonify, Response
from controllers.report_controller import generate_csv_report, get_dashboard_data
from routes.middleware import require_auth

report_bp = Blueprint('reports', __name__)


@report_bp.route('/dashboard', methods=['GET'])
@require_auth
def dashboard():
    """GET /api/dashboard - Dashboard stats."""
    result, status = get_dashboard_data()
    return jsonify(result), status


@report_bp.route('/export', methods=['GET'])
@require_auth
def export_csv():
    """GET /api/reports/export?type=products|transactions - Download CSV."""
    report_type = request.args.get('type', 'products')
    csv_data, filename = generate_csv_report(report_type)
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )
