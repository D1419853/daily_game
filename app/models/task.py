from app.models.base import get_db_connection

class Task:
    @staticmethod
    def create(user_id, title, difficulty):
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO tasks (user_id, title, difficulty) VALUES (?, ?, ?)',
            (user_id, title, difficulty)
from .db import get_db_connection

class Task:
    @staticmethod
    def create(user_id, title, description, difficulty):
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO tasks (user_id, title, description, difficulty) VALUES (?, ?, ?, ?)',
            (user_id, title, description, difficulty)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_by_user(user_id):
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
    def complete(task_id):
        conn = get_db_connection()
        conn.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
    def update_status(task_id, is_completed):
        conn = get_db_connection()
        conn.execute('UPDATE tasks SET is_completed = ? WHERE id = ?', (is_completed, task_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(task_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()

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
