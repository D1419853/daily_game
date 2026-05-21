from app.models.database import get_db_connection
import sqlite3

class Achievement:
    """成就模型，處理成就設定與玩家解鎖紀錄"""

    @staticmethod
    def create(name, description, requirement_type, requirement_count, reward_coins, reward_title):
        """建立新成就設定 (後台使用)"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO achievements 
                   (name, description, requirement_type, requirement_count, reward_coins, reward_title) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (name, description, requirement_type, requirement_count, reward_coins, reward_title)
            )
            conn.commit()
            achievement_id = cursor.lastrowid
            return achievement_id
        except Exception as e:
            print(f"Error creating achievement: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得所有成就設定"""
        conn = get_db_connection()
        try:
            achievements = conn.execute('SELECT * FROM achievements').fetchall()
            return [dict(a) for a in achievements]
        except Exception as e:
            print(f"Error getting achievements: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(achievement_id):
        """根據 ID 取得單一成就設定"""
        conn = get_db_connection()
        try:
            achievement = conn.execute('SELECT * FROM achievements WHERE id = ?', (achievement_id,)).fetchone()
            return dict(achievement) if achievement else None
        except Exception as e:
            print(f"Error getting achievement by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_unlocked_by_user(user_id):
        """取得特定使用者已解鎖的所有成就"""
        conn = get_db_connection()
        try:
            query = '''
                SELECT a.*, ua.unlocked_at 
                FROM achievements a
                JOIN user_achievements ua ON a.id = ua.achievement_id
                WHERE ua.user_id = ?
                ORDER BY ua.unlocked_at DESC
            '''
            achievements = conn.execute(query, (user_id,)).fetchall()
            return [dict(a) for a in achievements]
        except Exception as e:
            print(f"Error getting unlocked achievements: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def unlock(user_id, achievement_id):
        """為使用者解鎖成就"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # 檢查是否已解鎖
            existing = cursor.execute(
                'SELECT * FROM user_achievements WHERE user_id = ? AND achievement_id = ?',
                (user_id, achievement_id)
            ).fetchone()
            
            if not existing:
                cursor.execute(
                    'INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)',
                    (user_id, achievement_id)
                )
                conn.commit()
            return True
        except Exception as e:
            print(f"Error unlocking achievement: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def update(achievement_id, name, description):
        """更新成就設定"""
        conn = get_db_connection()
        try:
            conn.execute(
                'UPDATE achievements SET name = ?, description = ? WHERE id = ?',
                (name, description, achievement_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating achievement: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(achievement_id):
        """刪除成就設定"""
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM achievements WHERE id = ?', (achievement_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting achievement: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
