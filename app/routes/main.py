from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.models.user import User
from app.models.task import Task
from app.models.monster import UserMonsterInstance
from app.models.item import Item
from app.models.achievement import Achievement
from functools import wraps

main_bp = Blueprint('main', __name__)

def login_required(view):
    """登入驗證裝飾器"""
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('請先登入後再進行此操作！', 'warning')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@main_bp.route('/')
@login_required
def index():
    """首頁 / 遊戲大廳"""
    user_id = session['user_id']
    
    # 1. 獲取使用者資訊 (包含角色等級、經驗值、金幣等)
    user = User.get_by_id(user_id)
    if not user:
        # 防呆，如果 session 存在但 DB 中無此人，清除 session 回登入頁
        session.clear()
        return redirect(url_for('auth.login'))

    # 2. 獲取當前遭遇怪物。若無，則自動為其遭遇一隻
    monster = UserMonsterInstance.get_current_for_user(user_id)
    if not monster:
        UserMonsterInstance.spawn_for_user(user_id)
        monster = UserMonsterInstance.get_current_for_user(user_id)

    # 3. 獲取當前裝備的武器
    equipped_weapon = Item.get_equipped_weapon(user_id)

    # 4. 獲取使用者的所有冒險任務
    tasks = Task.get_by_user(user_id)
    
    # 5. 計算任務進度與完成度
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t['status'] == 'completed'])

    return render_template(
        'index.html', 
        user=user, 
        monster=monster, 
        equipped_weapon=equipped_weapon,
        tasks=tasks, 
        total_tasks=total_tasks, 
        completed_tasks=completed_tasks
    )

@main_bp.route('/shop')
@login_required
def shop():
    """裝備商店與玩家背包"""
    user_id = session['user_id']
    
    user = User.get_by_id(user_id)
    items = Item.get_all()
    user_items = Item.get_user_items(user_id)
    
    return render_template(
        'shop.html',
        user=user,
        items=items,
        user_items=user_items
    )

@main_bp.route('/shop/buy/<int:item_id>', methods=['POST'])
@login_required
def buy_item(item_id):
    """玩家購買裝備商品"""
    user_id = session['user_id']
    
    success, message = Item.buy_item(user_id, item_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
        
    return redirect(url_for('main.shop'))

@main_bp.route('/shop/equip/<int:user_item_id>', methods=['POST'])
@login_required
def equip_item(user_item_id):
    """玩家裝備背包中的道具"""
    user_id = session['user_id']
    
    success, message = Item.equip_item(user_id, user_item_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
        
    return redirect(url_for('main.shop'))

@main_bp.route('/profile')
@login_required
def profile():
    """個人資料、成就牆與排行榜"""
    user_id = session['user_id']
    
    user = User.get_by_id(user_id)
    achievements = Achievement.get_all()
    unlocked_achievements = Achievement.get_unlocked_by_user(user_id)
    leaderboard = User.get_all()  # 依金幣/等級排序
    
    # 整理已解鎖成就的 ID 方便在範本中判斷亮起狀態
    unlocked_ids = {a['id'] for a in unlocked_achievements}
    
    return render_template(
        'profile.html',
        user=user,
        achievements=achievements,
        unlocked_ids=unlocked_ids,
        leaderboard=leaderboard
    )
