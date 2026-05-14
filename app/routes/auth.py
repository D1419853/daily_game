from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    顯示註冊頁面 (GET) 或 處理註冊邏輯 (POST)。
    POST 時需：
    1. 驗證使用者名稱是否唯一
    2. 加密密碼並存入 users 表
    3. 為新使用者建立初始角色 (Character) 與 第一隻怪物實體
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    顯示登入頁面 (GET) 或 處理登入邏輯 (POST)。
    POST 時需：
    1. 比對使用者名稱與密碼雜湊
    2. 存入 user_id 到 session
    """
    pass

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    清除 Session 並登出。
    """
    pass
