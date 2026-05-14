from flask import Flask
import os

def create_app():
    app = Flask(__name__, 
                instance_relative_config=True,
                template_folder='app/templates',
                static_folder='app/static')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    from app.routes.auth import auth_bp
    from app.routes.task import task_bp
    from app.routes.index import index_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(index_bp)

    return app

def init_db():
    """初始化資料庫 (建立資料表)"""
    import sqlite3
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
    import sqlite3
    db_path = 'instance/database.db'
    conn = sqlite3.connect(db_path)
    
    achievements = [
        ('新手冒險者', '擊敗第 1 隻怪物 (完成 1 個任務)', 'task_completed', 1, 100, '見習勇者'),
        ('十人斬', '累計擊敗 10 隻怪物', 'task_completed', 10, 500, '資深獵人'),
        ('屠龍者', '累計擊敗 50 隻怪物', 'task_completed', 50, 2000, '傳說英雄')
    ]
    
    cursor = conn.cursor()
    for ach in achievements:
        # 避免重複插入
        cursor.execute('SELECT id FROM achievements WHERE name = ?', (ach[0],))
        if cursor.fetchone() is None:
            cursor.execute('''INSERT INTO achievements 
                (name, description, requirement_type, requirement_count, reward_coins, reward_title) 
                VALUES (?, ?, ?, ?, ?, ?)''', ach)
    
    conn.commit()
    conn.close()
    print("初始成就資料已匯入。")

if __name__ == '__main__':
    app = create_app()
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    app.run(debug=True)
