from .db import get_db_connection
import sqlite3

class Monster:
    @staticmethod
    def get_all():
        """取得所有怪物範本。"""
        try:
            conn = get_db_connection()
            monsters = conn.execute('SELECT * FROM monsters').fetchall()
            conn.close()
            return monsters
        except sqlite3.Error as e:
            print(f"Error getting monsters: {e}")
            return []

    @staticmethod
    def get_by_id(monster_id):
        """根據 ID 取得怪物範本。"""
        try:
            conn = get_db_connection()
            monster = conn.execute('SELECT * FROM monsters WHERE id = ?', (monster_id,)).fetchone()
            conn.close()
            return monster
        except sqlite3.Error as e:
            print(f"Error getting monster by id: {e}")
            return None

class UserMonsterInstance:
    @staticmethod
    def get_current_for_user(user_id):
        """取得使用者目前遭遇的怪物實體。"""
        try:
            conn = get_db_connection()
            instance = conn.execute('''
                SELECT umi.*, m.name, m.max_hp as monster_max_hp, m.xp_reward, m.gold_reward, m.image_path
                FROM user_monster_instances umi
                JOIN monsters m ON umi.monster_id = m.id
                WHERE umi.user_id = ?
            ''', (user_id,)).fetchone()
            conn.close()
            return instance
        except sqlite3.Error as e:
            print(f"Error getting current monster instance: {e}")
            return None

    @staticmethod
    def create(user_id, monster_id):
        """為使用者建立一個新的怪物實體。"""
        try:
            conn = get_db_connection()
            monster = conn.execute('SELECT max_hp FROM monsters WHERE id = ?', (monster_id,)).fetchone()
            if not monster:
                return False
                
            conn.execute(
                'INSERT INTO user_monster_instances (user_id, monster_id, current_hp) VALUES (?, ?, ?)',
                (user_id, monster_id, monster['max_hp'])
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error creating monster instance: {e}")
            return False

    @staticmethod
    def damage_monster(user_id, damage):
        """
        對怪物造成傷害。
        :return: (True/False, is_dead)
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE user_monster_instances SET current_hp = current_hp - ? WHERE user_id = ?',
                (damage, user_id)
            )
            instance = conn.execute('SELECT current_hp FROM user_monster_instances WHERE user_id = ?', (user_id,)).fetchone()
            
            is_dead = False
            if instance and instance['current_hp'] <= 0:
                is_dead = True
                # 若死亡，移除此實體（後續路由會負責產生下一隻）
                conn.execute('DELETE FROM user_monster_instances WHERE user_id = ?', (user_id,))
            
            conn.commit()
            conn.close()
            return True, is_dead
        except sqlite3.Error as e:
            print(f"Error damaging monster: {e}")
            return False, False
