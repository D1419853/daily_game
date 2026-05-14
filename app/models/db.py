import sqlite3
import os

DB_PATH = os.path.join('instance', 'database.db')

def get_db_connection():
    # 確保 instance 資料夾存在
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓回傳結果可以像字典一樣存取
    return conn
