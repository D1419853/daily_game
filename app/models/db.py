import sqlite3
import os

# 確保對應的目錄存在
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance')
DB_PATH = os.path.join(DB_DIR, 'database.db')

def get_db_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # 讓回傳的資料可以用 dict 的方式透過 key 存取
    conn.row_factory = sqlite3.Row
    return conn
