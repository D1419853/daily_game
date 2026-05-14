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
from flask import Flask
import os
from app.models.base import init_db
from .models.db import get_db_connection

def create_app():
    app = Flask(__name__, instance_relative_config=True)
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
    from .routes.auth import auth_bp
    from .routes.tasks import tasks_bp
    from .routes.combat import combat_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(combat_bp)

    return app
    from .routes.main import main_bp
    from .routes.tasks import tasks_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(tasks_bp)

    return app

def init_db():
    """初始化資料庫並執行 schema.sql"""
    conn = get_db_connection()
    with open('database/schema.sql', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized successfully.")
