from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User
from ..models.character import Character
from ..models.monster import UserMonsterInstance, Monster

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊新帳號，並同時初始化角色與第一隻怪物。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('請填寫所有欄位')
            return render_template('auth/register.html')

        if User.get_by_username(username):
            flash('此使用者名稱已被使用')
            return render_template('auth/register.html')

        # 建立使用者
        password_hash = generate_password_hash(password)
        user_id = User.create(username, password_hash)
        
        if user_id:
            # 建立關聯角色數值
            Character.create_for_user(user_id)
            # 為使用者遭遇第一隻怪物 (預設為 ID 1)
            UserMonsterInstance.create(user_id, 1)
            
            flash('註冊成功，請登入')
            return redirect(url_for('auth.login'))
        else:
            flash('註冊失敗，系統錯誤')

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    使用者登入邏輯。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.get_by_username(username)
        
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('main.index'))
        else:
            flash('帳號或密碼錯誤')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    清除 Session 並重導向。
    """
    session.clear()
    return redirect(url_for('auth.login'))
