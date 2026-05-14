from flask import Flask
from app.routes import register_routes
from app.models.database import init_db

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    # 設定 SECRET_KEY，用於 session 安全 (正式環境應從環境變數讀取)
    app.config['SECRET_KEY'] = 'dev_secret_key_please_change_in_production'
    
    # 初始化資料庫
    with app.app_context():
        init_db()
    
    # 註冊所有的 Blueprint 路由
    register_routes(app)
    
    return app
