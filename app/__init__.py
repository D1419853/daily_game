import os
import sqlite3

def init_db():
    """初始化資料庫 (建立資料表)"""
    db_path = 'instance/database.db'
    schema_path = 'database/schema.sql'
    
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
        
    conn = sqlite3.connect(db_path)
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("資料庫初始化完成。")

def seed_db():
    """加入初始成就資料"""
    db_path = 'instance/database.db'
    conn = sqlite3.connect(db_path)
    
    achievements = [
        ('新手冒險者', '擊敗第 1 隻怪物 (完成 1 個任務)', 'task_completed', 1, 100, '見習勇者'),
        ('十人斬', '累計擊敗 10 隻怪物', 'task_completed', 10, 500, '資深獵人'),
        ('屠龍者', '累計擊敗 50 隻怪物', 'task_completed', 50, 2000, '傳說英雄')
    ]
    
    cursor = conn.cursor()
    for ach in achievements:
        cursor.execute('SELECT id FROM achievements WHERE name = ?', (ach[0],))
        if cursor.fetchone() is None:
            cursor.execute('''INSERT INTO achievements 
                (name, description, requirement_type, requirement_count, reward_coins, reward_title) 
                VALUES (?, ?, ?, ?, ?, ?)''', ach)
    
    conn.commit()
    conn.close()
    print("初始成就資料已匯入。")
