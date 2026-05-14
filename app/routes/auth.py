from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊。
    GET: 顯示註冊頁面。
    POST: 接收資料、雜湊密碼、建立帳號。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入。
    GET: 顯示登入頁面。
    POST: 驗證帳密、設定 Session。
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    處理使用者登出。
    清除 Session 並重導向回登入頁。
    """
    pass
