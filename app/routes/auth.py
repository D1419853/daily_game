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
