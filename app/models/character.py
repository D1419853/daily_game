from .db import get_db_connection
import sqlite3

class Character:
    @staticmethod
    def create_for_user(user_id):
        """
        為新使用者建立初始角色數值。
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO characters (user_id, level, xp, gold, hp, max_hp) VALUES (?, 1, 0, 0, 100, 100)',
                (user_id,)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error creating character: {e}")
            return False

    @staticmethod
    def get_by_user_id(user_id):
        """
        取得使用者的角色數值。
        """
        try:
            conn = get_db_connection()
            char = conn.execute('SELECT * FROM characters WHERE user_id = ?', (user_id,)).fetchone()
            conn.close()
            return char
        except sqlite3.Error as e:
            print(f"Error getting character: {e}")
            return None

    @staticmethod
    def add_rewards(user_id, xp_gain, gold_gain):
        """
        發放獎勵並檢查是否升級。
        """
        try:
            conn = get_db_connection()
            char = conn.execute('SELECT level, xp FROM characters WHERE user_id = ?', (user_id,)).fetchone()
            
            new_xp = char['xp'] + xp_gain
            new_level = char['level']
            
            # 簡易升級邏輯：每 100 經驗值升一級
            while new_xp >= 100:
                new_xp -= 100
                new_level += 1
            
            conn.execute(
                'UPDATE characters SET xp = ?, level = ?, gold = gold + ? WHERE user_id = ?',
                (new_xp, new_level, gold_gain, user_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error adding rewards: {e}")
            return False

    @staticmethod
    def update_hp(user_id, hp_change):
        """
        更新血量（例如被怪打或回血）。
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE characters SET hp = MAX(0, MIN(max_hp, hp + ?)) WHERE user_id = ?',
                (hp_change, user_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating HP: {e}")
            return False
