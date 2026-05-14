from app.models.db import get_db_connection

class User:
    @staticmethod
    def create(username, password_hash):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def update_stats(user_id, exp_gain):
        conn = get_db_connection()
        user = conn.execute("SELECT level, exp FROM users WHERE id = ?", (user_id,)).fetchone()
        if user:
            # 簡單升級邏輯：每 100 經驗值升 1 級
            new_exp = user['exp'] + exp_gain
            new_level = user['level'] + (new_exp // 100)
            new_exp = new_exp % 100
            
            conn.execute(
                "UPDATE users SET exp = ?, level = ? WHERE id = ?",
                (new_exp, new_level, user_id)
            )
            conn.commit()
        conn.close()
