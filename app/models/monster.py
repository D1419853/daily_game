from .db import get_db_connection

class Monster:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        monsters = conn.execute('SELECT * FROM monsters').fetchall()
        conn.close()
        return monsters

    @staticmethod
    def get_by_id(monster_id):
        conn = get_db_connection()
        monster = conn.execute('SELECT * FROM monsters WHERE id = ?', (monster_id,)).fetchone()
        conn.close()
        return monster

class UserMonsterInstance:
    @staticmethod
    def get_current_for_user(user_id):
        conn = get_db_connection()
        # 取得使用者目前正在打的那隻怪，包含怪物基本資料
        instance = conn.execute('''
            SELECT umi.*, m.name, m.max_hp as monster_max_hp, m.xp_reward, m.gold_reward, m.image_path
            FROM user_monster_instances umi
            JOIN monsters m ON umi.monster_id = m.id
            WHERE umi.user_id = ?
        ''', (user_id,)).fetchone()
        conn.close()
        return instance

    @staticmethod
    def create(user_id, monster_id):
        conn = get_db_connection()
        monster = conn.execute('SELECT max_hp FROM monsters WHERE id = ?', (monster_id,)).fetchone()
        conn.execute(
            'INSERT INTO user_monster_instances (user_id, monster_id, current_hp) VALUES (?, ?, ?)',
            (user_id, monster_id, monster['max_hp'])
        )
        conn.commit()
        conn.close()

    @staticmethod
    def damage_monster(user_id, damage):
        conn = get_db_connection()
        conn.execute(
            'UPDATE user_monster_instances SET current_hp = current_hp - ? WHERE user_id = ?',
            (damage, user_id)
        )
        conn.commit()
        conn.close()
