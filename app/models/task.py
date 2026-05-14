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
from app.models.base import get_db_connection

class Task:
    @staticmethod
    def create(user_id, title, difficulty):
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO tasks (user_id, title, difficulty) VALUES (?, ?, ?)',
            (user_id, title, difficulty)
from .db import get_db_connection
import sqlite3

class Task:
    @staticmethod
    def create(user_id, title, description, difficulty):
        """
        建立新任務。
        :param difficulty: 1 (Easy), 2 (Normal), 3 (Hard)
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO tasks (user_id, title, description, difficulty) VALUES (?, ?, ?, ?)',
                (user_id, title, description, difficulty)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error creating task: {e}")
            return False

    @staticmethod
    def get_all_by_user(user_id):
        """
        取得該使用者的所有任務。
        """
        try:
            conn = get_db_connection()
            tasks = conn.execute(
                'SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC', 
                (user_id,)
            ).fetchall()
            conn.close()
            return tasks
        except sqlite3.Error as e:
            print(f"Error getting tasks: {e}")
            return []

    @staticmethod
    def get_by_id(task_id):
        conn = get_db_connection()
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        conn.close()
        return task

    @staticmethod
    def complete(task_id):
        conn = get_db_connection()
        conn.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
    def update_status(task_id, is_completed):
        conn = get_db_connection()
        conn.execute('UPDATE tasks SET is_completed = ? WHERE id = ?', (is_completed, task_id))
        conn.commit()
        conn.close()
        """
        取得單筆任務。
        """
        try:
            conn = get_db_connection()
            task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
            conn.close()
            return task
        except sqlite3.Error as e:
            print(f"Error getting task by id: {e}")
            return None

    @staticmethod
    def update(task_id, title, description, difficulty):
        """
        更新任務內容。
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE tasks SET title = ?, description = ?, difficulty = ? WHERE id = ?',
                (title, description, difficulty, task_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating task: {e}")
            return False

    @staticmethod
    def delete(task_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
    def get_by_id(task_id):
        conn = get_db_connection()
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        conn.close()
        return task
    def update_status(task_id, is_completed):
        """
        更新任務完成狀態。
        """
        try:
            conn = get_db_connection()
            conn.execute('UPDATE tasks SET is_completed = ? WHERE id = ?', (is_completed, task_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating task status: {e}")
            return False

    @staticmethod
    def delete(task_id):
        """
        刪除任務。
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting task: {e}")
            return False
