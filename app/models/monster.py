from app.models.db import get_db_connection

class Monster:
    @staticmethod
    def get_active_monster():
        conn = get_db_connection()
        monster = conn.execute("SELECT * FROM monsters WHERE is_active = 1 LIMIT 1").fetchone()
        conn.close()
        return dict(monster) if monster else None

    @staticmethod
    def create(name, max_hp, image_path='', is_active=0):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO monsters (name, max_hp, current_hp, image_path, is_active) VALUES (?, ?, ?, ?, ?)",
            (name, max_hp, max_hp, image_path, is_active)
        )
        conn.commit()
        monster_id = cursor.lastrowid
        conn.close()
        return monster_id

    @staticmethod
    def take_damage(monster_id, damage):
        conn = get_db_connection()
        monster = conn.execute("SELECT current_hp FROM monsters WHERE id = ?", (monster_id,)).fetchone()
        if monster:
            new_hp = max(0, monster['current_hp'] - damage)
            conn.execute("UPDATE monsters SET current_hp = ? WHERE id = ?", (new_hp, monster_id))
            conn.commit()
        conn.close()
