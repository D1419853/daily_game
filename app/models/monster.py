from app.models.database import get_db_connection
import random

class Monster:
    @staticmethod
    def get_all():
        """取得所有怪物範本"""
        conn = get_db_connection()
        try:
            monsters = conn.execute("SELECT * FROM monsters").fetchall()
            return [dict(m) for m in monsters]
        except Exception as e:
            print(f"Error getting monsters: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(monster_id):
        """依 ID 取得怪物範本"""
        conn = get_db_connection()
        try:
            monster = conn.execute("SELECT * FROM monsters WHERE id = ?", (monster_id,)).fetchone()
            return dict(monster) if monster else None
        except Exception as e:
            print(f"Error getting monster by id: {e}")
            return None
        finally:
            conn.close()


class UserMonsterInstance:
    @staticmethod
    def get_current_for_user(user_id):
        """取得使用者目前遭遇的怪物實體資訊"""
        conn = get_db_connection()
        try:
            query = """
                SELECT umi.id, umi.user_id, umi.monster_id, umi.current_hp,
                       m.name, m.max_hp, m.xp_reward, m.gold_reward, m.image_path
                FROM user_monster_instances umi
                JOIN monsters m ON umi.monster_id = m.id
                WHERE umi.user_id = ?
            """
            instance = conn.execute(query, (user_id,)).fetchone()
            return dict(instance) if instance else None
        except Exception as e:
            print(f"Error getting current monster instance: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def spawn_for_user(user_id):
        """為使用者隨機遭遇一隻新怪物"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            # 1. 取得所有怪物範本
            cursor.execute("SELECT * FROM monsters")
            monsters = cursor.fetchall()
            if not monsters:
                return False
                
            # 2. 隨機挑選一隻
            chosen = random.choice(monsters)
            
            # 3. 先清空當前使用者的怪物實體 (防呆)
            cursor.execute("DELETE FROM user_monster_instances WHERE user_id = ?", (user_id,))
            
            # 4. 插入新怪物實體
            cursor.execute(
                "INSERT INTO user_monster_instances (user_id, monster_id, current_hp) VALUES (?, ?, ?)",
                (user_id, chosen['id'], chosen['max_hp'])
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error spawning monster: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def damage_monster(user_id, damage):
        """
        對當前怪物造成傷害
        回傳值: (success_bool, is_dead_bool)
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # 1. 取得當前怪物實體
            cursor.execute("SELECT id, current_hp FROM user_monster_instances WHERE user_id = ?", (user_id,))
            instance = cursor.fetchone()
            if not instance:
                return False, False
                
            new_hp = max(0, instance['current_hp'] - damage)
            is_dead = (new_hp <= 0)
            
            if is_dead:
                # 怪物被消滅，直接移除實體
                cursor.execute("DELETE FROM user_monster_instances WHERE user_id = ?", (user_id,))
            else:
                # 更新血量
                cursor.execute(
                    "UPDATE user_monster_instances SET current_hp = ? WHERE user_id = ?",
                    (new_hp, user_id)
                )
                
            conn.commit()
            return True, is_dead
        except Exception as e:
            print(f"Error damaging monster: {e}")
            conn.rollback()
            return False, False
        finally:
            conn.close()
