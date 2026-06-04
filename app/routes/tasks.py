from flask import Blueprint, request, redirect, url_for, flash, session
from app.models.task import Task
from app.models.monster import UserMonsterInstance, Monster
from app.models.item import Item
from app.models.user import User
from app.models.achievement import Achievement
from functools import wraps

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def login_required(view):
    """登入驗證裝飾器"""
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('請先登入後再進行此操作！', 'warning')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    """發佈新的冒險任務"""
    user_id = session['user_id']
    title = request.form.get('title')
    description = request.form.get('description', '')
    difficulty = request.form.get('difficulty', 1)
    duration_minutes = request.form.get('duration_minutes', 0)
    
    try:
        difficulty = int(difficulty)
    except ValueError:
        difficulty = 1

    try:
        duration_minutes = int(duration_minutes)
    except ValueError:
        duration_minutes = 0

    if not title:
        flash('任務名稱不能為空', 'danger')
        return redirect(url_for('main.index'))

    task_id = Task.create(user_id, title, description, difficulty, duration_minutes)
    if task_id:
        flash('冒險任務發佈成功！一隻新的怪物被召喚了 👾。', 'success')
    else:
        flash('任務發佈失敗，請重試', 'danger')
        
    return redirect(url_for('main.index'))

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """撤回/刪除任務"""
    user_id = session['user_id']
    task = Task.get_by_id(task_id)

    if not task or task['user_id'] != user_id:
        flash('找不到該任務或您無權限操作', 'danger')
        return redirect(url_for('main.index'))

    if Task.delete(task_id):
        flash('任務已成功撤回。', 'info')
    else:
        flash('任務刪除失敗', 'danger')

    return redirect(url_for('main.index'))

@tasks_bp.route('/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    """完成任務並攻擊怪物"""
    user_id = session['user_id']
    task = Task.get_by_id(task_id)

    if not task or task['user_id'] != user_id:
        flash('無效的任務操作', 'danger')
        return redirect(url_for('main.index'))

    if task['status'] == 'completed':
        flash('該任務已經完成過了！', 'warning')
        return redirect(url_for('main.index'))

    from datetime import datetime
    if task.get('unlock_at'):
        unlock_time = datetime.strptime(task['unlock_at'], "%Y-%m-%d %H:%M:%S")
        if datetime.now() < unlock_time:
            flash('任務計時尚未結束，還不能完成！', 'warning')
            return redirect(url_for('main.index'))

    # 1. 標記任務為已完成
    Task.mark_completed(task_id)

    # 2. 計算傷害
    # 簡單: 15, 普通: 35, 困難: 60
    damage_map = {1: 15, 2: 35, 3: 60}
    base_damage = damage_map.get(task['difficulty'], 15)
    
    # 檢查是否穿戴武器
    equipped_weapon = Item.get_equipped_weapon(user_id)
    weapon_bonus = equipped_weapon['bonus_stat'] if equipped_weapon else 0
    total_damage = base_damage + weapon_bonus

    # 3. 取得當前怪物，並造成傷害
    monster = UserMonsterInstance.get_current_for_user(user_id)
    if not monster:
        # 若沒有怪物，先防呆遭遇一隻
        UserMonsterInstance.spawn_for_user(user_id)
        monster = UserMonsterInstance.get_current_for_user(user_id)

    success, is_dead = UserMonsterInstance.damage_monster(user_id, total_damage)
    
    if success:
        if is_dead:
            # 怪物死亡！發放獎勵
            xp_reward = monster['xp_reward']
            gold_reward = monster['gold_reward']
            
            import random
            extra_msg = ""
            if random.random() < 0.3:  # 30% 機率獲得額外獎勵
                bonus_gold = random.randint(20, 100)
                gold_reward += bonus_gold
                extra_msg = f" 🎁 運氣爆棚！怪物掉落了額外寶藏，多獲得 🪙 {bonus_gold} 金幣！"

            res = User.add_rewards(user_id, xp_reward, gold_reward)
            
            # 紀錄擊敗到圖鑑中
            Monster.record_defeat(user_id, monster['monster_id'])
            
            # 生成新怪物
            UserMonsterInstance.spawn_for_user(user_id)
            
            flash(f"⚔️ 任務完成！對 {monster['name']} 造成 {total_damage} 點致命一擊！", 'success')
            flash(f"🎉 成功擊敗 {monster['name']}！獲得 {xp_reward} EXP 與 🪙 {gold_reward} 金幣！{extra_msg}", 'success')
            
            if res and res.get('leveled_up'):
                flash(f"🌟 恭喜升級！您已達到了等級 {res['new_level']}！", 'info')

            # 4. 檢查成就解鎖
            all_achievements = Achievement.get_all()
            unlocked = Achievement.get_unlocked_by_user(user_id)
            unlocked_ids = {a['id'] for a in unlocked}
            
            user_tasks = Task.get_by_user(user_id)
            completed_count = len([t for t in user_tasks if t['status'] == 'completed'])
            
            for ach in all_achievements:
                if ach['id'] not in unlocked_ids:
                    if ach['requirement_type'] == 'task_completed' and completed_count >= ach['requirement_count']:
                        # 解鎖成就
                        Achievement.unlock(user_id, ach['id'])
                        # 發放成就額外金幣
                        User.add_rewards(user_id, 0, ach['reward_coins'])
                        # 更新頭銜
                        User.update_character(user_id, current_title=ach['reward_title'])
                        flash(f"🏆 解鎖成就：{ach['name']}！獲得 🪙 {ach['reward_coins']} 金幣與稱號「{ach['reward_title']}」！", 'gold')
            return redirect(url_for('main.index', effect='kill'))
        else:
            # 怪物沒死，普通傷害
            flash(f"⚔️ 任務完成！對 {monster['name']} 造成 {total_damage} 點傷害！(HP: {max(0, monster['current_hp'] - total_damage)}/{monster['max_hp']})", 'success')
            return redirect(url_for('main.index', effect='damage'))
    else:
        flash('攻擊失敗，系統錯誤', 'danger')

    return redirect(url_for('main.index'))
