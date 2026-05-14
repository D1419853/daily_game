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
