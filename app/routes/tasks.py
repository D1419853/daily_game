from flask import Blueprint, render_template, redirect, url_for, request, flash, session

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks/add', methods=['POST'])
def add_task():
    user_id = session.get('user_id')
    if not user_id: return redirect(url_for('auth.login'))
    
    title = request.form['title']
    difficulty = int(request.form['difficulty'])
    
    from app.models.task import Task
    Task.create(user_id, title, difficulty)
    flash(f'任務「{title}」已發佈！', 'info')
    return redirect(url_for('combat.index'))

@tasks_bp.route('/tasks/edit/<int:task_id>', methods=['GET'])
def edit_task_page(task_id):
    """
    顯示編輯任務頁面。
    """
    pass

@tasks_bp.route('/tasks/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    """
    更新任務內容。
    """
    pass

@tasks_bp.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    from app.models.task import Task
    Task.delete(task_id)
    flash('任務已撤回。', 'secondary')
    return redirect(url_for('combat.index'))

@tasks_bp.route('/tasks/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    user_id = session.get('user_id')
    if not user_id: return redirect(url_for('auth.login'))
    
    from app.models.task import Task
    from app.models.monster import Monster
    from app.models.user import User
    
    task = Task.get_by_id(task_id)
    if task and task['status'] == 'pending':
        # 1. 標記任務完成
        Task.complete(task_id)
        
        # 2. 計算傷害 (1:10, 2:30, 3:50)
        damage_map = {1: 10, 2: 30, 3: 50}
        damage = damage_map.get(task['difficulty'], 10)
        
        # 3. 扣除怪物 HP
        monster = Monster.get_current_for_user(user_id)
        if monster:
            res = Monster.take_damage(monster['id'], damage)
            flash(f'任務完成！對 {monster["name"]} 造成了 {damage} 點傷害！', 'success')
            
            # 4. 檢查怪物是否死亡
            if res['is_alive'] == 0:
                # 給予獎勵 (簡單怪物給 20 exp, 10 gold)
                exp_gain = 20
                gold_gain = 10
                User.update_progress(user_id, exp_gain, gold_gain)
                flash(f'擊敗了 {monster["name"]}！獲得 {exp_gain} EXP 與 {gold_gain} 金幣！', 'warning')
                # 生成新怪物
                Monster.spawn_for_user(user_id)
                
    return redirect(url_for('combat.index'))
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..models.task import Task
from ..models.character import Character
from ..models.monster import UserMonsterInstance, Monster
import random

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks')
def list_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    tasks = Task.get_all_by_user(session['user_id'])
    return render_template('tasks/list.html', tasks=tasks)

@tasks_bp.route('/tasks/new', methods=['GET'])
def new_task():
    return render_template('tasks/new.html')

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    title = request.form.get('title')
    description = request.form.get('description')
    difficulty = int(request.form.get('difficulty', 1))
    
    if not title:
        flash('任務標題不能為空')
        return redirect(url_for('tasks.new_task'))
        
    Task.create(session['user_id'], title, description, difficulty)
    flash('任務建立成功！')
    return redirect(url_for('tasks.list_tasks'))

@tasks_bp.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """
    完成任務並對怪物造成傷害。
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    task = Task.get_by_id(task_id)
    
    if not task or task['user_id'] != user_id:
        flash('找不到該任務')
        return redirect(url_for('tasks.list_tasks'))
        
    if task['is_completed']:
        flash('任務已經完成過了')
        return redirect(url_for('tasks.list_tasks'))
        
    # 1. 更新任務狀態
    Task.update_status(task_id, True)
    
    # 2. 計算傷害 (難度越高傷害越高)
    damage = task['difficulty'] * 20
    
    # 3. 對怪物造成傷害
    success, is_dead = UserMonsterInstance.damage_monster(user_id, damage)
    
    if success:
        # 4. 發放獎勵
        xp_gain = task['difficulty'] * 10
        gold_gain = task['difficulty'] * 5
        Character.add_rewards(user_id, xp_gain, gold_gain)
        
        flash(f'任務完成！造成 {damage} 點傷害，獲得 {xp_gain} 經驗值與 {gold_gain} 金幣！')
        
        # 5. 若怪物死亡，產生下一隻
        if is_dead:
            flash('太棒了！你擊敗了怪物！下一隻強敵出現了！')
            # 隨機挑選下一隻怪物範本
            all_monsters = Monster.get_all()
            next_monster = random.choice(all_monsters)
            UserMonsterInstance.create(user_id, next_monster['id'])
            
    return redirect(url_for('main.index'))

@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    Task.delete(task_id)
    flash('任務已刪除')
    return redirect(url_for('tasks.list_tasks'))
