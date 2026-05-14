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
