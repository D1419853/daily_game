import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線"""
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓回傳的資料可以直接用字典方式存取欄位
    return conn

def init_db():
    """初始化資料庫與資料表"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if not os.path.exists(schema_path):
        return

    conn = get_db_connection()
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
