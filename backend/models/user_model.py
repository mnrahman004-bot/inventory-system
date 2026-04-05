# backend/models/user_model.py
# User model - handles all DB operations for the users table

from config.db import get_db_connection, close_connection

class UserModel:

    @staticmethod
    def find_by_username(username):
        """Fetch a user record by username."""
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cursor.fetchone()
        except Exception as e:
            print(f"[UserModel] find_by_username error: {e}")
            return None
        finally:
            close_connection(conn, cursor)

    @staticmethod
    def create_user(username, password_hash):
        """Insert a new user into the database."""
        conn = get_db_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )
            return True
        except Exception as e:
            print(f"[UserModel] create_user error: {e}")
            return False
        finally:
            close_connection(conn, cursor)
