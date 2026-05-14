import sqlite3
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
