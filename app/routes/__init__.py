from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.task_routes import task_bp

def register_routes(app: Flask):
    """
    註冊所有的 Blueprint 到 Flask App
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
