# backend/models/transaction_model.py
# Transaction model - handles stock IN/OUT history

from config.db import get_db_connection, close_connection

class TransactionModel:

    @staticmethod
    def get_all():
        """Fetch all transactions joined with product names."""
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT t.id, t.product_id, p.name AS product_name,
                       t.type, t.quantity, t.date
                FROM transactions t
                JOIN products p ON t.product_id = p.id
                ORDER BY t.date DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"[TransactionModel] get_all error: {e}")
            return []
        finally:
            close_connection(conn, cursor)

    @staticmethod
    def create(product_id, tx_type, quantity):
        """Insert a new transaction record."""
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO transactions (product_id, type, quantity) VALUES (%s, %s, %s)",
                (product_id, tx_type, quantity)
            )
            return cursor.lastrowid
        except Exception as e:
            print(f"[TransactionModel] create error: {e}")
            return None
        finally:
            close_connection(conn, cursor)

    @staticmethod
    def get_by_product(product_id):
        """Fetch all transactions for a specific product (used by ML)."""
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT type, quantity, date
                FROM transactions
                WHERE product_id = %s
                ORDER BY date ASC
            """, (product_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"[TransactionModel] get_by_product error: {e}")
            return []
        finally:
            close_connection(conn, cursor)

    @staticmethod
    def get_recent_sales_vs_purchases(days=30):
        """Return grouped IN/OUT totals for the last N days (bar chart)."""
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT DATE(date) as day, type, SUM(quantity) as total
                FROM transactions
                WHERE date >= DATE_SUB(NOW(), INTERVAL %s DAY)
                GROUP BY DATE(date), type
                ORDER BY day ASC
            """, (days,))
            return cursor.fetchall()
        except Exception as e:
            print(f"[TransactionModel] get_recent_sales_vs_purchases error: {e}")
            return []
        finally:
            close_connection(conn, cursor)
