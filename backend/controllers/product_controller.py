# backend/controllers/product_controller.py
# Business logic for product CRUD operations

from models.product_model import ProductModel


def get_all_products():
    """Return all products."""
    products = ProductModel.get_all()
    # Convert Decimal to float for JSON serialization
    for p in products:
        if p.get('price'):
            p['price'] = float(p['price'])
        if p.get('created_at'):
            p['created_at'] = str(p['created_at'])
    return {'products': products}, 200


def get_product(product_id):
    """Return a single product."""
    product = ProductModel.get_by_id(product_id)
    if not product:
        return {'error': 'Product not found'}, 404
    product['price'] = float(product['price'])
    product['created_at'] = str(product['created_at'])
    return {'product': product}, 200


def create_product(data):
    """Validate and create a new product."""
    name = data.get('name', '').strip()
    category = data.get('category', '').strip()
    price = data.get('price')
    quantity = data.get('quantity')

    # Validation
    if not name:
        return {'error': 'Product name is required'}, 400
    if not category:
        return {'error': 'Category is required'}, 400
    try:
        price = float(price)
        quantity = int(quantity)
        if price < 0 or quantity < 0:
            raise ValueError()
    except (TypeError, ValueError):
        return {'error': 'Price and quantity must be non-negative numbers'}, 400

    product_id = ProductModel.create(name, category, price, quantity)
    if product_id is None:
        return {'error': 'Failed to create product'}, 500

    return {'message': 'Product created', 'id': product_id}, 201


def update_product(product_id, data):
    """Validate and update an existing product."""
    existing = ProductModel.get_by_id(product_id)
    if not existing:
        return {'error': 'Product not found'}, 404

    name = data.get('name', existing['name']).strip()
    category = data.get('category', existing['category']).strip()

    try:
        price = float(data.get('price', existing['price']))
        quantity = int(data.get('quantity', existing['quantity']))
        if price < 0 or quantity < 0:
            raise ValueError()
    except (TypeError, ValueError):
        return {'error': 'Price and quantity must be non-negative numbers'}, 400

    success = ProductModel.update(product_id, name, category, price, quantity)
    if not success:
        return {'error': 'Failed to update product'}, 500

    return {'message': 'Product updated'}, 200


def delete_product(product_id):
    """Delete a product by ID."""
    existing = ProductModel.get_by_id(product_id)
    if not existing:
        return {'error': 'Product not found'}, 404

    success = ProductModel.delete(product_id)
    if not success:
        return {'error': 'Failed to delete product'}, 500

    return {'message': 'Product deleted'}, 200
