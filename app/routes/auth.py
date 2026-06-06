from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.models.monster import UserMonsterInstance

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """處理使用者註冊"""
    if 'user_id' in session:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password')

        if not username or not password:
            flash('請填寫帳號與密碼', 'danger')
            return render_template('auth/register.html')

        existing_user = User.get_by_username(username)
        if existing_user:
            flash('此帳號已被使用，請換一個', 'warning')
            return render_template('auth/register.html')

        # 1. 加密密碼並建立使用者
        password_hash = generate_password_hash(password)
        user_id = User.create(username, password_hash)
        
        if user_id:
            # 2. 自動為該玩家遭遇第一隻怪物
            UserMonsterInstance.spawn_for_user(user_id)
            flash('註冊成功！歡迎加入勇者行列，請登入！', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('註冊失敗，系統錯誤', 'danger')

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """處理使用者登入"""
    if 'user_id' in session:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password')

        if not username or not password:
            flash('請填寫帳號與密碼', 'danger')
            return render_template('auth/login.html')

        user = User.get_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session.permanent = True   # 讓 session 在瀏覽器關閉後仍然存在
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('歡迎回來，冒險者！準備好迎接挑戰了嗎？', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('帳號或密碼錯誤，請重新輸入', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """處理使用者登出"""
    session.clear()
    flash('您已成功離開冒險，期待您的再次歸來！', 'info')
    return redirect(url_for('auth.login'))
