from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """顯示登入頁面與處理登入邏輯"""
    # GET: 返回登入模板
    # POST: 驗證使用者並重導向
    pass

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """顯示註冊頁面與處理註冊邏輯"""
    # GET: 返回註冊模板
    # POST: 建立使用者並重導向
    pass

@auth_bp.route('/logout')
def logout():
    """登出使用者並清除 Session"""
    pass
