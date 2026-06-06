from flask import Flask
import os
from datetime import timedelta
from app.models.database import init_db

def create_app():
    # 使用正確的 static 和 templates 資料夾路徑
    app = Flask(__name__, 
                instance_relative_config=True,
                template_folder='templates',
                static_folder='static')
    
    app.config.from_mapping(
        SECRET_KEY='dev_secret_key_please_change_in_production',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
        PERMANENT_SESSION_LIFETIME=timedelta(days=30),  # session 保存 30 天
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化資料庫 (如果不存在會自動建立並匯入預填資料)
    with app.app_context():
        init_db()

    # 註冊 Blueprints
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(main_bp)

    return app
