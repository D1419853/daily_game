import sqlite3
import os
from flask import current_app

def get_db_connection():
    """建立與 SQLite 資料庫的連線"""
    db_path = os.path.join(current_app.instance_path, 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class Achievement:
    """成就模型，處理成就設定與玩家解鎖紀錄"""

    @staticmethod
    def create(name, description, requirement_type, requirement_count, reward_coins, reward_title):
        """建立新成就設定 (後台使用)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO achievements 
                   (name, description, requirement_type, requirement_count, reward_coins, reward_title) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (name, description, requirement_type, requirement_count, reward_coins, reward_title)
            )
            conn.commit()
            achievement_id = cursor.lastrowid
            conn.close()
            return achievement_id
        except Exception as e:
            print(f"Error creating achievement: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有成就設定"""
        try:
            conn = get_db_connection()
            achievements = conn.execute('SELECT * FROM achievements').fetchall()
            conn.close()
            return achievements
        except Exception as e:
            print(f"Error getting achievements: {e}")
            return []

    @staticmethod
    def get_by_id(achievement_id):
        """根據 ID 取得單一成就設定"""
        try:
            conn = get_db_connection()
            achievement = conn.execute('SELECT * FROM achievements WHERE id = ?', (achievement_id,)).fetchone()
            conn.close()
            return achievement
        except Exception as e:
            print(f"Error getting achievement by id: {e}")
            return None

    @staticmethod
    def get_unlocked_by_user(user_id):
        """取得特定使用者已解鎖的所有成就"""
        try:
            conn = get_db_connection()
            query = '''
                SELECT a.*, ua.unlocked_at 
                FROM achievements a
                JOIN user_achievements ua ON a.id = ua.achievement_id
                WHERE ua.user_id = ?
                ORDER BY ua.unlocked_at DESC
            '''
            achievements = conn.execute(query, (user_id,)).fetchall()
            conn.close()
            return achievements
        except Exception as e:
            print(f"Error getting unlocked achievements: {e}")
            return []

    @staticmethod
    def unlock(user_id, achievement_id):
        """為使用者解鎖成就"""
        try:
            conn = get_db_connection()
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
            conn.close()
            return True
        except Exception as e:
            print(f"Error unlocking achievement: {e}")
            return False

    @staticmethod
    def update(achievement_id, name, description):
        """更新成就設定"""
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE achievements SET name = ?, description = ? WHERE id = ?',
                (name, description, achievement_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating achievement: {e}")
            return False

    @staticmethod
    def delete(achievement_id):
        """刪除成就設定"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM achievements WHERE id = ?', (achievement_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting achievement: {e}")
            return False
