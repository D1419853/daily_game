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
