from flask import Blueprint, render_template, request, redirect, url_for, session, flash

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/', methods=['GET'])
def list_tasks():
    """渲染使用者的所有任務列表"""
    pass

@tasks_bp.route('/new', methods=['GET'])
def new_task_page():
    """渲染新增任務表單頁面"""
    pass

@tasks_bp.route('/', methods=['POST'])
def create_task():
    """處理建立任務邏輯，將資料存入 DB，重導向至 /tasks"""
    pass

@tasks_bp.route('/<int:task_id>/edit', methods=['GET'])
def edit_task_page(task_id):
    """渲染編輯特定任務的表單頁面"""
    pass

@tasks_bp.route('/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    """處理更新任務邏輯，更新 DB，重導向至 /tasks"""
    pass

@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """處理刪除任務邏輯，重導向至 /tasks"""
    pass

@tasks_bp.route('/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """
    處理任務完成邏輯：
    1. 將任務狀態標記為完成
    2. 扣除當前怪物血量
    3. 結算使用者經驗值並判斷升級
    處理完畢後重導向回首頁，並提示成功訊息。
    """
    pass
