import sqlite3

def get_db_connection():
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

class Achievement:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        achievements = conn.execute('SELECT * FROM achievements').fetchall()
        conn.close()
        return achievements

    @staticmethod
    def get_unlocked_by_user(user_id):
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

    @staticmethod
    def unlock(user_id, achievement_id):
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
