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
        """
        刪除使用者。
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
            return False
