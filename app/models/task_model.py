from app.models.database import get_db_connection

class TaskModel:
    @staticmethod
    def create_task(user_id, title, description="", target=1):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tasks (user_id, title, description, target, progress, status)
            VALUES (?, ?, ?, ?, 0, 'pending')
            """,
            (user_id, title, description, target)
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id

    @staticmethod
    def get_tasks_by_user(user_id):
        conn = get_db_connection()
        tasks = conn.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,)).fetchall()
        conn.close()
        return [dict(task) for task in tasks]

    @staticmethod
    def get_task_by_id(task_id):
        conn = get_db_connection()
        task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        conn.close()
        return dict(task) if task else None

    @staticmethod
    def add_progress(task_id, amount=1):
        conn = get_db_connection()
        task = conn.execute("SELECT progress, target, status FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not task or task['status'] == 'completed':
            conn.close()
            return False

        new_progress = task['progress'] + amount
        new_status = 'completed' if new_progress >= task['target'] else 'pending'

        conn.execute(
            "UPDATE tasks SET progress = ?, status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (new_progress, new_status, task_id)
        )
        conn.commit()
        conn.close()
        return new_status == 'completed'

    @staticmethod
    def reset_daily_tasks(user_id):
        """清空進度並重置為未完成"""
        conn = get_db_connection()
        conn.execute(
            "UPDATE tasks SET progress = 0, status = 'pending', updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
            (user_id,)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete_all_tasks(user_id):
        """刪除所有任務 (用於刷新任務時)"""
        conn = get_db_connection()
        conn.execute("DELETE FROM tasks WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
