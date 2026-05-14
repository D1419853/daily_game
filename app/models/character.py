from .db import get_db_connection

class Character:
    @staticmethod
    def create_for_user(user_id):
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO characters (user_id, level, xp, gold, hp, max_hp) VALUES (?, 1, 0, 0, 100, 100)',
            (user_id,)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db_connection()
        char = conn.execute('SELECT * FROM characters WHERE user_id = ?', (user_id,)).fetchone()
        conn.close()
        return char

    @staticmethod
    def add_rewards(user_id, xp_gain, gold_gain):
        conn = get_db_connection()
        conn.execute(
            'UPDATE characters SET xp = xp + ?, gold = gold + ? WHERE user_id = ?',
            (xp_gain, gold_gain, user_id)
        )
        conn.commit()
        conn.close()
        # 這裡之後可以加入檢查升級的邏輯
