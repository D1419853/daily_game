from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    遊戲首頁 (大廳)。
    1. 需檢查登入狀態
    2. 取得角色資訊與當前怪物資訊
    3. 渲染 index.html
    """
    pass
