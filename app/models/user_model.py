from app.models.database import get_db_connection

class UserModel:
    @staticmethod
    def create_user(username, password_hash):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_user_by_username(username):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def update_login_date(user_id, date_str):
        conn = get_db_connection()
        conn.execute("UPDATE users SET last_login_date = ? WHERE id = ?", (date_str, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def add_exp_and_coins(user_id, exp_gain, coins_gain):
        conn = get_db_connection()
        user = conn.execute("SELECT level, exp, coins FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user:
            conn.close()
            return False

        new_exp = user['exp'] + exp_gain
        new_coins = user['coins'] + coins_gain
        new_level = user['level']
        
        # 簡單升級邏輯：每 100 exp 升 1 級
        while new_exp >= new_level * 100:
            new_exp -= new_level * 100
            new_level += 1

        conn.execute(
            "UPDATE users SET level = ?, exp = ?, coins = ? WHERE id = ?",
            (new_level, new_exp, new_coins, user_id)
        )
        conn.commit()
        conn.close()
        return True
