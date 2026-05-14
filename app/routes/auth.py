from flask import Blueprint, render_template, redirect, url_for, request, flash, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        from app.models.user import User
        user = User.get_by_username(username)
        
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('歡迎回來，冒險者！', 'success')
            return redirect(url_for('combat.index'))
        
        flash('帳號或密碼錯誤。', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        from app.models.user import User
        if User.get_by_username(username):
            flash('此帳號已被註冊。', 'warning')
        elif User.create(username, password):
            # 自動生成第一隻怪物
            user = User.get_by_username(username)
            from app.models.monster import Monster
            Monster.spawn_for_user(user['id'])
            
            flash('註冊成功！請登入。', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('註冊失敗，請稍後再試。', 'danger')
            
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('您已離開冒險。', 'info')
    return redirect(url_for('auth.login'))
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
