import sqlite3

def get_db_connection():
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

class User:
    @staticmethod
    def create(username, email, password_hash):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        return user
        
    @staticmethod
    def update_coins_and_title(user_id, extra_coins, new_title=None):
        conn = get_db_connection()
        if new_title:
            conn.execute('UPDATE users SET coins = coins + ?, current_title = ? WHERE id = ?', (extra_coins, new_title, user_id))
        else:
            conn.execute('UPDATE users SET coins = coins + ? WHERE id = ?', (extra_coins, user_id))
        conn.commit()
        conn.close()
