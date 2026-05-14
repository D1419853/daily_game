from app.models.database import get_db_connection
import sqlite3

class UserModel:
    @staticmethod
    def create(data):
        """
        新增一筆使用者記錄。
        :param data: dict，包含 'username' 與 'password_hash'
        :return: 新增的資料 ID，若失敗則回傳 None
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (data['username'], data['password_hash'])
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating user: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有使用者記錄。
        :return: 使用者字典的清單
        """
        conn = get_db_connection()
        try:
            users = conn.execute("SELECT * FROM users").fetchall()
            return [dict(user) for user in users]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """
        取得單筆使用者記錄。
        :param user_id: 使用者 ID
        :return: 使用者字典，找不到則回傳 None
        """
        conn = get_db_connection()
        try:
            user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(user_id, data):
        """
        更新使用者記錄。
        :param user_id: 使用者 ID
        :param data: dict，要更新的欄位與值
        :return: 布林值，表示是否成功
        """
        conn = get_db_connection()
        try:
            # 動態產生 UPDATE 語句
            set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
            values = list(data.values())
            values.append(user_id)
            
            conn.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(user_id):
        """
        刪除使用者記錄。
        :param user_id: 使用者 ID
        :return: 布林值，表示是否成功
        """
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    # --- 以下為特製邏輯 ---
    
    @staticmethod
    def get_by_username(username):
        """依據帳號名稱取得使用者"""
        conn = get_db_connection()
        try:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def add_exp_and_coins(user_id, exp_gain, coins_gain):
        """發放經驗值與金幣，並處理升級邏輯"""
        user = UserModel.get_by_id(user_id)
        if not user:
            return False

        new_exp = user['exp'] + exp_gain
        new_coins = user['coins'] + coins_gain
        new_level = user['level']
        
        while new_exp >= new_level * 100:
            new_exp -= new_level * 100
            new_level += 1

        return UserModel.update(user_id, {
            'level': new_level,
            'exp': new_exp,
            'coins': new_coins
        })
