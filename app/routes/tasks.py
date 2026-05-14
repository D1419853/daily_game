from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..models.task import Task
from ..models.character import Character
from ..models.monster import UserMonsterInstance

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def list_tasks():
    """
    列出使用者的所有任務。
    """
    pass

@tasks_bp.route('/new', methods=['GET', 'POST'])
def add_task():
    """
    新增任務的表單頁面與儲存邏輯。
    """
    pass

@tasks_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    """
    編輯既有任務。
    """
    pass

@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    刪除任務。
    """
    pass

@tasks_bp.route('/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """
    核心邏輯：標記任務完成 -> 扣除怪物血量 -> 給予角色獎勵 -> 檢查怪物死亡與升級。
    """
    pass
