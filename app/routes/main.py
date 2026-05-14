from flask import Blueprint, render_template, session, redirect, url_for
from ..models.character import Character
from ..models.monster import UserMonsterInstance

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    遊戲主首頁。
    顯示：
    1. 角色數值 (HP, Level, XP, Gold)
    2. 當前怪物資訊 (血量、圖片)
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    character = Character.get_by_user_id(user_id)
    monster_instance = UserMonsterInstance.get_current_for_user(user_id)
    
    return render_template('index.html', character=character, monster=monster_instance)
