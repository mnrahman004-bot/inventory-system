# backend/controllers/report_controller.py
# Generates CSV export of all products + transactions

import csv
import io
from models.product_model import ProductModel
from models.transaction_model import TransactionModel


def generate_csv_report(report_type='products'):
    """
    Generate a CSV report.
    report_type: 'products' | 'transactions'
    Returns: (csv_string, filename)
    """
    output = io.StringIO()

    if report_type == 'transactions':
        transactions = TransactionModel.get_all()
        writer = csv.DictWriter(output, fieldnames=[
            'id', 'product_id', 'product_name', 'type', 'quantity', 'date'
        ])
        writer.writeheader()
        for t in transactions:
            writer.writerow({
                'id': t['id'],
                'product_id': t['product_id'],
                'product_name': t.get('product_name', ''),
                'type': t['type'],
                'quantity': t['quantity'],
                'date': str(t['date'])
            })
        filename = 'transactions_report.csv'

    else:  # default: products
        products = ProductModel.get_all()
        writer = csv.DictWriter(output, fieldnames=[
            'id', 'name', 'category', 'price', 'quantity', 'stock_value', 'created_at'
        ])
        writer.writeheader()
        for p in products:
            writer.writerow({
                'id': p['id'],
                'name': p['name'],
                'category': p['category'],
                'price': float(p['price']),
                'quantity': p['quantity'],
                'stock_value': round(float(p['price']) * p['quantity'], 2),
                'created_at': str(p['created_at'])
            })
        filename = 'products_report.csv'

    return output.getvalue(), filename


def get_dashboard_data():
    """Aggregate dashboard statistics."""
    stats = ProductModel.get_dashboard_stats()
    category_dist = ProductModel.get_category_distribution()

    # Serialize Decimal values
    if stats:
        stats['total_stock_value'] = float(stats.get('total_stock_value') or 0)

    return {
        'stats': stats,
        'category_distribution': category_dist
    }, 200
