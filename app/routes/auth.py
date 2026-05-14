from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET'])
def register_page():
    """渲染註冊頁面"""
    pass

@auth_bp.route('/register', methods=['POST'])
def register():
    """處理註冊邏輯，驗證成功後重導向至 /login"""
    pass

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """渲染登入頁面"""
    pass

@auth_bp.route('/login', methods=['POST'])
def login():
    """處理登入邏輯，成功後儲存 Session 並重導向至 /"""
    pass

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """處理登出邏輯，清除 session 並重導向至 /login"""
    pass
