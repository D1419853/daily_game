from app.models.base import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def create(username, password):
        conn = get_db_connection()
        password_hash = generate_password_hash(password)
        try:
            conn.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def update_progress(user_id, exp_gain, gold_gain):
        conn = get_db_connection()
        user = conn.execute('SELECT level, exp FROM users WHERE id = ?', (user_id,)).fetchone()
        if user:
            new_exp = user['exp'] + exp_gain
            new_level = user['level']
            # Simple level up logic: 100 exp per level
            while new_exp >= 100:
                new_exp -= 100
                new_level += 1
            
            conn.execute(
                'UPDATE users SET level = ?, exp = ?, gold = gold + ? WHERE id = ?',
                (new_level, new_exp, gold_gain, user_id)
            )
            conn.commit()
        conn.close()
