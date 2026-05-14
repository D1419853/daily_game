from flask import Blueprint, render_template, redirect, url_for, request, flash, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入。
    GET: 渲染登入頁面。
    POST: 驗證帳號密碼，成功則跳轉至首頁。
    """
    pass

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊。
    GET: 渲染註冊頁面。
    POST: 建立新使用者，成功則跳轉至登入頁。
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    登出使用者，清除 Session。
    """
    pass
