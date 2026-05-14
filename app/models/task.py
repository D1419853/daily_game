import sqlite3
from datetime import datetime

class TaskModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def create(self, user_id, title, category, difficulty):
        query = """
        INSERT INTO tasks (user_id, title, category, difficulty)
        VALUES (?, ?, ?, ?)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id, title, category, difficulty))
            conn.commit()
            return cursor.lastrowid

    def get_all_by_user(self, user_id):
        query = "SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            return cursor.fetchall()

    def get_by_id(self, task_id):
        query = "SELECT * FROM tasks WHERE id = ?"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, (task_id,))
            return cursor.fetchone()

    def update_status(self, task_id, status):
        query = "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (status, datetime.now().isoformat(), task_id))
            conn.commit()

    def delete(self, task_id):
        query = "DELETE FROM tasks WHERE id = ?"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (task_id,))
            conn.commit()
