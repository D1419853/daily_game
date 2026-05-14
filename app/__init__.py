from flask import Flask
import os
from app.models.base import init_db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

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
