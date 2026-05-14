from app.models.db import get_db_connection

class Task:
    @staticmethod
    def create(user_id, title, description='', exp_reward=10, damage=10):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (user_id, title, description, exp_reward, damage) VALUES (?, ?, ?, ?, ?)",
            (user_id, title, description, exp_reward, damage)
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id

    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        tasks = conn.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
        conn.close()
        return [dict(t) for t in tasks]

    @staticmethod
    def get_by_id(task_id):
        conn = get_db_connection()
        task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        conn.close()
        return dict(task) if task else None

    @staticmethod
    def complete(task_id):
        conn = get_db_connection()
        conn.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def update(task_id, title, description):
        conn = get_db_connection()
        conn.execute(
            "UPDATE tasks SET title = ?, description = ? WHERE id = ?",
            (title, description, task_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(task_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
