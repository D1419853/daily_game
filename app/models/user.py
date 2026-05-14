import sqlite3
import os
from flask import current_app

def get_db_connection():
    """建立與 SQLite 資料庫的連線"""
    db_path = os.path.join(current_app.instance_path, 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class User:
    """使用者模型，處理玩家帳號與屬性"""

    @staticmethod
    def create(username, email, password_hash):
        """建立新使用者"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有使用者"""
        try:
            conn = get_db_connection()
            users = conn.execute('SELECT * FROM users').fetchall()
            conn.close()
            return users
        except Exception as e:
            print(f"Error getting users: {e}")
            return []

    @staticmethod
    def get_by_id(user_id):
        """根據 ID 取得單一使用者"""
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            conn.close()
            return user
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None

    @staticmethod
    def get_by_email(email):
        """根據 Email 取得單一使用者"""
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            conn.close()
            return user
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None

    @staticmethod
    def update(user_id, coins=None, current_title=None):
        """更新使用者金幣或稱號"""
        try:
            conn = get_db_connection()
            if coins is not None and current_title is not None:
                conn.execute('UPDATE users SET coins = ?, current_title = ? WHERE id = ?', (coins, current_title, user_id))
            elif coins is not None:
                conn.execute('UPDATE users SET coins = ? WHERE id = ?', (coins, user_id))
            elif current_title is not None:
                conn.execute('UPDATE users SET current_title = ? WHERE id = ?', (current_title, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    @staticmethod
    def delete(user_id):
        """刪除使用者"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
