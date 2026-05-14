from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    渲染首頁（遊戲主畫面）。
    - 需檢查是否已登入
    - 取得使用者狀態、當前怪物狀態與未完成的任務列表
    """
    pass

@main_bp.route('/stats', methods=['GET'])
def stats():
    """
    渲染個人數據統計頁面。
    - 顯示等級、經驗值與歷史成就
    """
    pass
