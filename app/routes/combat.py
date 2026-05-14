from flask import Blueprint, render_template, redirect, url_for, session

combat_bp = Blueprint('combat', __name__)

@combat_bp.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    from app.models.user import User
    from app.models.monster import Monster
    from app.models.task import Task
    
    user = User.get_by_id(user_id)
    monster = Monster.get_current_for_user(user_id)
    tasks = Task.get_all_by_user(user_id)
    
    return render_template('index.html', user=user, monster=monster, tasks=tasks)

@combat_bp.route('/shop')
def shop():
    return render_template('shop.html')
