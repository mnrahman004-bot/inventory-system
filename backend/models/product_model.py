# backend/models/product_model.py
# Product model - CRUD operations for the products table

from config.db import get_db_connection, close_connection

class ProductModel:

    @staticmethod
    def get_all():
        """Fetch all products."""
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM products ORDER BY created_at DESC")
            return cursor.fetchall()
        except Exception as e:
            print(f"[ProductModel] get_all error: {e}")
            return []
        finally:
            close_connection(conn, cursor)

    @staticmethod
    def get_by_id(product_id):
        """Fetch a single product by ID."""
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"[ProductModel] get_by_id error: {e}")
            return None
        finally:
            close_connection(conn, cursor)

    @staticmethod
    def create(name, category, price, quantity):
        """Insert a new product."""
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO products (name, category, price, quantity) VALUES (%s, %s, %s, %s)",
                (name, category, price, quantity)
            )
            return cursor.lastrowid
        except Exception as e:
            print(f"[ProductModel] create error: {e}")
            return None
        finally:
            close_connection(conn, cursor)

    @staticmethod
    def update(product_id, name, category, price, quantity):
        """Update an existing product."""
        conn = get_db_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE products SET name=%s, category=%s, price=%s, quantity=%s WHERE id=%s",
                (name, category, price, quantity, product_id)
            )
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[ProductModel] update error: {e}")
            return False
        finally:
            close_connection(conn, cursor)

    @staticmethod
    def delete(product_id):
        """Delete a product by ID."""
        conn = get_db_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[ProductModel] delete error: {e}")
            return False
        finally:
            close_connection(conn, cursor)

    @staticmethod
    def update_quantity(product_id, delta):
        """
        Adjust stock quantity by delta (+/-).
        Returns False if result would be negative.
        """
        conn = get_db_connection()
        if not conn:
            return False
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT quantity FROM products WHERE id = %s FOR UPDATE", (product_id,))
            row = cursor.fetchone()
            if not row:
                return False
            new_qty = row['quantity'] + delta
            if new_qty < 0:
                return False  # Prevent negative stock
            cursor.execute("UPDATE products SET quantity = %s WHERE id = %s", (new_qty, product_id))
            return True
        except Exception as e:
            print(f"[ProductModel] update_quantity error: {e}")
            return False
        finally:
            close_connection(conn, cursor)

    @staticmethod
    def get_dashboard_stats():
        """Return aggregated stats for the dashboard."""
        conn = get_db_connection()
        if not conn:
            return {}
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT
                    COUNT(*) AS total_products,
                    SUM(price * quantity) AS total_stock_value,
                    SUM(CASE WHEN quantity < 10 THEN 1 ELSE 0 END) AS low_stock_count
                FROM products
            """)
            return cursor.fetchone()
        except Exception as e:
            print(f"[ProductModel] get_dashboard_stats error: {e}")
            return {}
        finally:
            close_connection(conn, cursor)

    @staticmethod
    def get_category_distribution():
        """Return count of products per category for pie chart."""
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT category, COUNT(*) as count, SUM(quantity) as total_qty
                FROM products GROUP BY category
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"[ProductModel] get_category_distribution error: {e}")
            return []
        finally:
            close_connection(conn, cursor)
