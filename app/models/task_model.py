from app.models.database import get_db_connection

class TaskModel:
    @staticmethod
    def create(data):
        """
        新增一筆任務記錄。
        :param data: dict，包含 user_id, title, description, target
        :return: 新增的資料 ID，若失敗則回傳 None
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (user_id, title, description, target, progress, status)
                VALUES (?, ?, ?, ?, 0, 'pending')
                """,
                (data['user_id'], data['title'], data.get('description', ''), data.get('target', 1))
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating task: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有任務記錄。
        :return: 任務字典的清單
        """
        conn = get_db_connection()
        try:
            tasks = conn.execute("SELECT * FROM tasks").fetchall()
            return [dict(task) for task in tasks]
        except Exception as e:
            print(f"Error getting all tasks: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(task_id):
        """
        取得單筆任務記錄。
        :param task_id: 任務 ID
        :return: 任務字典，找不到則回傳 None
        """
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
    def update(task_id, data):
        """
        更新任務記錄。
        :param task_id: 任務 ID
        :param data: dict，要更新的欄位與值
        :return: 布林值，表示是否成功
        """
        conn = get_db_connection()
        try:
            set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
            values = list(data.values())
            values.append(task_id)
            
            # 自動更新 updated_at
            if "updated_at" not in data:
                set_clause += ", updated_at = CURRENT_TIMESTAMP"
            
            conn.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating task: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(task_id):
        """
        刪除任務記錄。
        :param task_id: 任務 ID
        :return: 布林值，表示是否成功
        """
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

    # --- 以下為特製邏輯 ---

    @staticmethod
    def get_by_user(user_id):
        """取得特定使用者的所有任務"""
        conn = get_db_connection()
        try:
            tasks = conn.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,)).fetchall()
            return [dict(task) for task in tasks]
        except Exception as e:
            print(f"Error getting tasks by user: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def add_progress(task_id, amount=1):
        """增加任務進度，若達標則更新為 completed"""
        task = TaskModel.get_by_id(task_id)
        if not task or task['status'] == 'completed':
            return False

        new_progress = task['progress'] + amount
        new_status = 'completed' if new_progress >= task['target'] else 'pending'

        return TaskModel.update(task_id, {
            'progress': new_progress,
            'status': new_status
        })

    @staticmethod
    def reset_daily_tasks(user_id):
        """清空進度並重置為未完成"""
        conn = get_db_connection()
        try:
            conn.execute(
                "UPDATE tasks SET progress = 0, status = 'pending', updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
                (user_id,)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error resetting daily tasks: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def delete_all_tasks(user_id):
        """刪除特定使用者的所有任務 (用於刷新任務時)"""
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM tasks WHERE user_id = ?", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting all tasks: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
