from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import UserModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入：
    GET: 顯示登入表單
    POST: 接收 username 與 password，驗證後寫入 session，重導向至 /
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('請填寫帳號與密碼', 'danger')
            return redirect(url_for('auth.login'))
            
        user = UserModel.get_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('登入成功！', 'success')
            return redirect(url_for('tasks.index'))
        else:
            flash('帳號或密碼錯誤', 'danger')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊：
    GET: 顯示註冊表單
    POST: 接收表單建立新使用者，重導向至 /login
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('請填寫帳號與密碼', 'danger')
            return redirect(url_for('auth.register'))
            
        existing_user = UserModel.get_by_username(username)
        if existing_user:
            flash('此帳號已被使用', 'danger')
            return redirect(url_for('auth.register'))
            
        password_hash = generate_password_hash(password)
        user_id = UserModel.create({'username': username, 'password_hash': password_hash})
        
        if user_id:
            flash('註冊成功！請登入', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('發生錯誤，註冊失敗', 'danger')
            return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    """
    處理使用者登出：
    清除 session 內的登入狀態，重導向至 /login
    """
    session.clear()
    flash('您已成功登出', 'info')
    return redirect(url_for('auth.login'))
