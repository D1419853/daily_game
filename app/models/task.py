import sqlite3
import os
from datetime import datetime
from flask import current_app

def get_db_connection():
    """建立與 SQLite 資料庫的連線"""
    db_path = os.path.join(current_app.instance_path, 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class Task:
    """任務模型，處理打怪任務的增刪改查"""

    @staticmethod
    def create(user_id, title):
        """建立新任務"""
        try:
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
        except Exception as e:
            print(f"Error creating task: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有任務"""
        try:
            conn = get_db_connection()
            tasks = conn.execute('SELECT * FROM tasks').fetchall()
            conn.close()
            return tasks
        except Exception as e:
            print(f"Error getting all tasks: {e}")
            return []

    @staticmethod
    def get_by_user(user_id):
        """取得特定使用者的所有任務"""
        try:
            conn = get_db_connection()
            tasks = conn.execute(
                'SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC', 
                (user_id,)
            ).fetchall()
            conn.close()
            return tasks
        except Exception as e:
            print(f"Error getting tasks by user: {e}")
            return []

    @staticmethod
    def get_by_id(task_id):
        """根據 ID 取得單一任務"""
        try:
            conn = get_db_connection()
            task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
            conn.close()
            return task
        except Exception as e:
            print(f"Error getting task by id: {e}")
            return None

    @staticmethod
    def mark_completed(task_id):
        """標記任務為已完成 (打怪成功)"""
        try:
            conn = get_db_connection()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute(
                'UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?',
                ('completed', now, task_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error completing task: {e}")
            return False

    @staticmethod
    def update(task_id, title):
        """更新任務標題"""
        try:
            conn = get_db_connection()
            conn.execute('UPDATE tasks SET title = ? WHERE id = ?', (title, task_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating task: {e}")
            return False

    @staticmethod
    def delete(task_id):
        """刪除任務"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False
