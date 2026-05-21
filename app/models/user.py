from app.models.database import get_db_connection
import sqlite3

class User:
    @staticmethod
    def create(username, password_hash):
        """建立新使用者並同時初始化勇者角色"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # 1. 插入使用者帳號
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            user_id = cursor.lastrowid
            
            # 2. 初始化勇者角色屬性
            cursor.execute(
                "INSERT INTO characters (user_id, level, xp, gold, current_title) VALUES (?, 1, 0, 0, '新手冒險者')",
                (user_id,)
            )
            
            conn.commit()
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """取得單一勇者及其角色狀態"""
        conn = get_db_connection()
        try:
            query = """
                SELECT u.id, u.username, c.level, c.xp, c.gold, c.current_title, u.created_at
                FROM users u
                JOIN characters c ON u.id = c.user_id
                WHERE u.id = ?
            """
            user = conn.execute(query, (user_id,)).fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_username(username):
        """僅取得帳密資訊以供登入驗證"""
        conn = get_db_connection()
        try:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得所有勇者列表 (用於排行榜)"""
        conn = get_db_connection()
        try:
            query = """
                SELECT u.id, u.username, c.level, c.xp, c.gold, c.current_title
                FROM users u
                JOIN characters c ON u.id = c.user_id
                ORDER BY c.gold DESC, c.level DESC
            """
            users = conn.execute(query).fetchall()
            return [dict(u) for u in users]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update_character(user_id, gold=None, xp=None, level=None, current_title=None):
        """彈性更新勇者屬性"""
        conn = get_db_connection()
        try:
            updates = []
            values = []
            if gold is not None:
                updates.append("gold = ?")
                values.append(gold)
            if xp is not None:
                updates.append("xp = ?")
                values.append(xp)
            if level is not None:
                updates.append("level = ?")
                values.append(level)
            if current_title is not None:
                updates.append("current_title = ?")
                values.append(current_title)
                
            if not updates:
                return False
                
            values.append(user_id)
            query = f"UPDATE characters SET {', '.join(updates)} WHERE user_id = ?"
            conn.execute(query, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating character: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def add_rewards(user_id, xp_gain, gold_gain):
        """給予經驗值與金幣獎勵，並處理升級邏輯"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # 1. 取得當前屬性
            cursor.execute("SELECT level, xp, gold FROM characters WHERE user_id = ?", (user_id,))
            char = cursor.fetchone()
            if not char:
                return False
                
            current_level = char['level']
            current_xp = char['xp']
            current_gold = char['gold']
            
            # 2. 計算新數值
            new_xp = current_xp + xp_gain
            new_gold = current_gold + gold_gain
            new_level = current_level
            
            # 3. 升級邏輯：每級所需經驗值為 level * 100
            xp_required = new_level * 100
            leveled_up = False
            while new_xp >= xp_required:
                new_xp -= xp_required
                new_level += 1
                xp_required = new_level * 100
                leveled_up = True
                
            # 4. 更新資料庫
            cursor.execute(
                "UPDATE characters SET level = ?, xp = ?, gold = ? WHERE user_id = ?",
                (new_level, new_xp, new_gold, user_id)
            )
            conn.commit()
            return {"leveled_up": leveled_up, "new_level": new_level, "xp_gain": xp_gain, "gold_gain": gold_gain}
        except Exception as e:
            print(f"Error adding rewards: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
