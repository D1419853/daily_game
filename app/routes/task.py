from flask import Blueprint, request, redirect, url_for, session, flash
from app.models.task import Task
from app.models.achievement import Achievement
from app.models.user import User

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks', methods=['POST'])
def add_task():
    """新增任務 (打怪任務)"""
    # 接收表單標題，呼叫 Task.create
    pass

@task_bp.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """標記任務完成並檢查成就"""
    # 1. 標記完成
    # 2. 檢查成就邏輯
    # 3. 發放獎勵
    pass

@task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """刪除指定任務"""
    # 呼叫 Task.delete
    pass
