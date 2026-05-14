from app.models.base import get_db_connection
import random

class Monster:
    @staticmethod
    def spawn_for_user(user_id):
        conn = get_db_connection()
        # Randomly choose a monster type
        types = [
            {'name': '小史萊姆', 'type': 'slime', 'hp': 50, 'img': '/static/images/slime.png'},
            {'name': '森林野狼', 'type': 'wolf', 'hp': 100, 'img': '/static/images/wolf.png'},
            {'name': '惡毒蝙蝠', 'type': 'bat', 'hp': 80, 'img': '/static/images/bat.png'}
        ]
        m = random.choice(types)
        
        conn.execute(
            'INSERT INTO monsters (user_id, name, monster_type, max_hp, current_hp, image_url) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, m['name'], m['type'], m['hp'], m['hp'], m['img'])
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_current_for_user(user_id):
        conn = get_db_connection()
        monster = conn.execute(
            'SELECT * FROM monsters WHERE user_id = ? AND is_alive = 1 ORDER BY created_at DESC LIMIT 1',
            (user_id,)
        ).fetchone()
        conn.close()
        return monster

    @staticmethod
    def take_damage(monster_id, damage):
        conn = get_db_connection()
        monster = conn.execute('SELECT current_hp, user_id FROM monsters WHERE id = ?', (monster_id,)).fetchone()
        if monster:
            new_hp = max(0, monster['current_hp'] - damage)
            is_alive = 1 if new_hp > 0 else 0
            conn.execute(
                'UPDATE monsters SET current_hp = ?, is_alive = ? WHERE id = ?',
                (new_hp, is_alive, monster_id)
            )
            conn.commit()
            conn.close()
            return {'new_hp': new_hp, 'is_alive': is_alive, 'user_id': monster['user_id']}
        conn.close()
        return None
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
