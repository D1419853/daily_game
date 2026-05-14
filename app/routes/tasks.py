from flask import Blueprint, render_template, request, redirect, url_for, session

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks')
def list_tasks():
    """
    顯示使用者的任務列表。
    """
    pass

@tasks_bp.route('/tasks/new', methods=['GET'])
def new_task():
    """
    顯示新增任務表單。
    """
    pass

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    執行新增任務，將資料存入資料庫。
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET'])
def edit_task(task_id):
    """
    顯示編輯任務表單。
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    """
    執行更新任務邏輯。
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    執行刪除任務。
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """
    關鍵邏輯：
    1. 標記任務完成
    2. 根據任務難度計算傷害，扣除當前怪物血量
    3. 發放經驗值與金幣給角色
    4. 檢查怪物是否死亡，若死亡則產生下一隻
    """
    pass
