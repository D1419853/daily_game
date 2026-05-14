from flask import Blueprint, request, redirect, url_for, session, flash, g
from app.models.task import Task
from app.models.achievement import Achievement
from app.models.user import User
from functools import wraps

task_bp = Blueprint('task', __name__)

def login_required(view):
    """登入驗證裝飾器"""
    @wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            flash('請先登入後再進行操作', 'warning')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@task_bp.route('/tasks', methods=['POST'])
@login_required
def add_task():
    """新增任務 (打怪任務)"""
    title = request.form.get('title')
    user_id = session.get('user_id')

    if not title:
        flash('請輸入任務名稱', 'danger')
    else:
        Task.create(user_id, title)
        flash('成功召喚了一隻怪物！(任務已新增)', 'success')

    return redirect(url_for('index.index'))

@task_bp.route('/tasks/<int:task_id>/complete', methods=['POST'])
@login_required
def complete_task(task_id):
    """標記任務完成並檢查成就 (擊敗怪物)"""
    user_id = session.get('user_id')
    task = Task.get_by_id(task_id)

    if task and task['user_id'] == user_id:
        # 1. 標記任務完成
        Task.mark_completed(task_id)
        flash('恭喜！你擊敗了怪物！', 'success')

        # 2. 檢查成就邏輯 (此處為範例邏輯：完成一項任務就解鎖第一個成就)
        # 實務上應根據 DB 中的 achievements 設定來檢查
        all_achievements = Achievement.get_all()
        user_tasks = Task.get_by_user(user_id)
        completed_count = len([t for t in user_tasks if t['status'] == 'completed'])

        for ach in all_achievements:
            if ach['requirement_type'] == 'task_completed' and completed_count >= ach['requirement_count']:
                # 檢查是否已解鎖過
                unlocked = Achievement.get_unlocked_by_user(user_id)
                if not any(u['id'] == ach['id'] for u in unlocked):
                    Achievement.unlock(user_id, ach['id'])
                    # 發放獎勵
                    user = User.get_by_id(user_id)
                    new_coins = user['coins'] + ach['reward_coins']
                    User.update(user_id, coins=new_coins, current_title=ach['reward_title'])
                    flash(f"解鎖成就：{ach['name']}！獲得 {ach['reward_coins']} 金幣與稱號「{ach['reward_title']}」！", 'gold')
    else:
        flash('操作無效', 'danger')

    return redirect(url_for('index.index'))

@task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """刪除任務"""
    user_id = session.get('user_id')
    task = Task.get_by_id(task_id)

    if task and task['user_id'] == user_id:
        Task.delete(task_id)
        flash('任務已刪除', 'info')
    else:
        flash('操作無效', 'danger')

    return redirect(url_for('index.index'))
