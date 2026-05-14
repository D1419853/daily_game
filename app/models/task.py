import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

class Task:
    @staticmethod
    def create(user_id, title):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (user_id, title) VALUES (?, ?)',
            (user_id, title)
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id

    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        tasks = conn.execute('SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
        conn.close()
        return tasks

    @staticmethod
    def get_by_id(task_id):
        conn = get_db_connection()
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        conn.close()
        return task

    @staticmethod
    def mark_completed(task_id):
        conn = get_db_connection()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            'UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?',
            ('completed', now, task_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(task_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
