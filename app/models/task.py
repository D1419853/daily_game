from app.models.database import get_db_connection
from datetime import datetime, timedelta

class Task:
    @staticmethod
    def create(user_id, title, description='', difficulty=1, duration_minutes=0):
        """新增一個冒險任務"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            unlock_at = None
            if duration_minutes > 0:
                unlock_at_dt = datetime.now() + timedelta(minutes=duration_minutes)
                unlock_at = unlock_at_dt.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                "INSERT INTO tasks (user_id, title, description, difficulty, status, duration_minutes, unlock_at) VALUES (?, ?, ?, ?, 'pending', ?, ?)",
                (user_id, title, description, difficulty, duration_minutes, unlock_at)
            )
            task_id = cursor.lastrowid
            conn.commit()
            return task_id
        except Exception as e:
            print(f"Error creating task: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(task_id):
        """取得特定任務"""
        conn = get_db_connection()
        try:
            task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            return dict(task) if task else None
        except Exception as e:
            print(f"Error getting task by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_user(user_id):
        """取得該使用者的所有任務"""
        conn = get_db_connection()
        try:
            tasks = conn.execute(
                "SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC", 
                (user_id,)
            ).fetchall()
            return [dict(t) for t in tasks]
        except Exception as e:
            print(f"Error getting tasks by user: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def mark_completed(task_id):
        """標記任務完成，記錄完成時間"""
        conn = get_db_connection()
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute(
                "UPDATE tasks SET status = 'completed', completed_at = ? WHERE id = ?",
                (now, task_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error marking task completed: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(task_id):
        """刪除任務"""
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
