from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """處理使用者註冊"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        error = None

        if not username:
            error = '請輸入使用者名稱'
        elif not email:
            error = '請輸入 Email'
        elif not password:
            error = '請輸入密碼'
        elif User.get_by_email(email) is not None:
            error = f"Email {email} 已經被註冊過了"

        if error is None:
            User.create(username, email, generate_password_hash(password))
            flash('註冊成功！現在可以登入了', 'success')
            return redirect(url_for('auth.login'))

        flash(error, 'danger')

    return render_template('login.html', mode='register')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """處理使用者登入"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        error = None
        user = User.get_by_email(email)

        if user is None:
            error = 'Email 不正確'
        elif not check_password_hash(user['password_hash'], password):
            error = '密碼不正確'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f"歡迎回來, {user['username']}!", 'success')
            return redirect(url_for('index.index'))

        flash(error, 'danger')

    return render_template('login.html', mode='login')

@auth_bp.route('/logout')
def logout():
    """處理使用者登出"""
    session.clear()
    flash('你已經成功登出', 'info')
    return redirect(url_for('auth.login'))
