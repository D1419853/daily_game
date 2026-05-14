from flask import Blueprint, render_template, session, redirect, url_for
from app.models.task import Task
from app.models.user import User
from app.models.achievement import Achievement

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    """首頁：顯示任務列表與遊戲狀態概覽"""
    user_id = session.get('user_id')
    
    if user_id is None:
        return redirect(url_for('auth.login'))
    
    user = User.get_by_id(user_id)
    tasks = Task.get_by_user(user_id)
    
    # 計算進度
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t['status'] == 'completed'])
    
    return render_template('index.html', 
                           user=user, 
                           tasks=tasks, 
                           total_tasks=total_tasks, 
                           completed_tasks=completed_tasks)

@index_bp.route('/profile')
def profile():
    """個人資料頁：顯示已解鎖成就與稱號"""
    user_id = session.get('user_id')
    
    if user_id is None:
        return redirect(url_for('auth.login'))
        
    user = User.get_by_id(user_id)
    unlocked_achievements = Achievement.get_unlocked_by_user(user_id)
    
    return render_template('profile.html', 
                           user=user, 
                           unlocked_achievements=unlocked_achievements)

@index_bp.route('/leaderboard')
def leaderboard():
    """排行榜頁：依金幣排序顯示玩家"""
    user_id = session.get('user_id')
    
    if user_id is None:
        return redirect(url_for('auth.login'))
        
    # 這裡簡單處理：取得所有使用者並依金幣排序
    all_users = User.get_all()
    # 將 sqlite3.Row 轉為 dict 並排序
    leaderboard_data = sorted([dict(u) for u in all_users], key=lambda x: x['coins'], reverse=True)
    
    return render_template('profile.html', 
                           leaderboard=leaderboard_data, 
                           show_leaderboard=True)
