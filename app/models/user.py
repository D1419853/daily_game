from app.models.db import get_db_connection

class User:
    @staticmethod
    def create(username, password_hash):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def update_stats(user_id, exp_gain):
        conn = get_db_connection()
        user = conn.execute("SELECT level, exp FROM users WHERE id = ?", (user_id,)).fetchone()
        if user:
            # 簡單升級邏輯：每 100 經驗值升 1 級
            new_exp = user['exp'] + exp_gain
            new_level = user['level'] + (new_exp // 100)
            new_exp = new_exp % 100
            
            conn.execute(
                "UPDATE users SET exp = ?, level = ? WHERE id = ?",
                (new_exp, new_level, user_id)
            )
            conn.commit()
        conn.close()
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
from datetime import datetime

class UserModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def create(self, username, password_hash):
        query = """
        INSERT INTO users (username, password_hash)
        VALUES (?, ?)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (username, password_hash))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def get_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = ?"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            return cursor.fetchone()

    def get_by_username(self, username):
        query = "SELECT * FROM users WHERE username = ?"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, (username,))
            return cursor.fetchone()

    def update_stats(self, user_id, exp, gold, level, current_hp, max_hp):
        query = """
        UPDATE users 
        SET experience = ?, gold = ?, level = ?, current_monster_hp = ?, max_monster_hp = ?
        WHERE id = ?
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (exp, gold, level, current_hp, max_hp, user_id))
            conn.commit()

    def delete(self, user_id):
        query = "DELETE FROM users WHERE id = ?"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            conn.commit()
from app.models.base import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def create(username, password):
        conn = get_db_connection()
        password_hash = generate_password_hash(password)
        try:
            conn.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()
from .db import get_db_connection
import sqlite3

class User:
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def create(username, password_hash):
        """
        新增一位使用者。
        :param username: 使用者名稱
        :param password_hash: 加密後的密碼
        :return: 新建立的使用者 ID
        """
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            user_id = cur.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.Error as e:
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
    def get_by_username(username):
        """
        根據使用者名稱取得使用者資料。
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            conn.close()
            return user
        except sqlite3.Error as e:
            print(f"Error getting user by username: {e}")
            return None

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def update_progress(user_id, exp_gain, gold_gain):
        conn = get_db_connection()
        user = conn.execute('SELECT level, exp FROM users WHERE id = ?', (user_id,)).fetchone()
        if user:
            new_exp = user['exp'] + exp_gain
            new_level = user['level']
            # Simple level up logic: 100 exp per level
            while new_exp >= 100:
                new_exp -= 100
                new_level += 1
            
            conn.execute(
                'UPDATE users SET level = ?, exp = ?, gold = gold + ? WHERE id = ?',
                (new_level, new_exp, gold_gain, user_id)
            )
            conn.commit()
        conn.close()
        """
        根據 ID 取得使用者資料。
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            conn.close()
            return user
        except sqlite3.Error as e:
            print(f"Error getting user by id: {e}")
            return None

    @staticmethod
    def update_password(user_id, new_password_hash):
        """
        更新使用者密碼。
        """
        try:
            conn = get_db_connection()
            conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_password_hash, user_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating password: {e}")
            return False

    @staticmethod
    def delete(user_id):
        """刪除使用者"""
        """
        刪除使用者。
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
            return False
