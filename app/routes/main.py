from flask import Blueprint, render_template, request, redirect, url_for, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示任務清單、角色狀態與怪物狀態。
    需確認使用者已登入。
    """
    pass

@main_bp.route('/task/new', methods=['GET'])
def task_new():
    """顯示新增任務表單。"""
    pass

@main_bp.route('/task/add', methods=['POST'])
def task_add():
    """接收表單資料，呼叫 TaskModel 建立任務。"""
    pass

@main_bp.route('/task/edit/<int:id>', methods=['GET'])
def task_edit(id):
    """顯示編輯任務表單，載入既有資料。"""
    pass

@main_bp.route('/task/update/<int:id>', methods=['POST'])
def task_update(id):
    """接收更新資料，呼叫 TaskModel 更新任務。"""
    pass

@main_bp.route('/task/delete/<int:id>', methods=['POST'])
def task_delete(id):
    """呼叫 TaskModel 刪除任務。"""
    pass

@main_bp.route('/task/complete/<int:id>', methods=['POST'])
def task_complete(id):
    """
    標記任務完成，並計算獎勵與打怪傷害。
    更新 Task 狀態與 User 狀態。
    """
    pass

@main_bp.route('/shop')
def shop():
    """顯示商城頁面與道具清單。"""
    pass

@main_bp.route('/shop/buy/<int:id>', methods=['POST'])
def buy_item(id):
    """處理購買邏輯：檢查金幣、扣款、加入背包。"""
    pass

@main_bp.route('/stats')
def stats():
    """顯示數據統計圖表頁面。"""
    pass
