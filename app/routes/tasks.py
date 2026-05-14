from flask import Blueprint, render_template, redirect, url_for, request, flash, session

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks/add', methods=['POST'])
def add_task():
    """
    新增任務。
    接收表單資料並呼叫 Task.create()。
    """
    pass

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
    """
    刪除任務。
    """
    pass

@tasks_bp.route('/tasks/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    """
    標記任務完成並觸發戰鬥邏輯。
    1. 標記任務 status 為 completed
    2. 呼叫 Combat 邏輯扣除怪物 HP
    """
    pass
