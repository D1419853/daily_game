from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入：
    GET: 顯示登入表單 (templates/auth/login.html)
    POST: 接收 username 與 password，驗證後寫入 session，重導向至 /
    """
    pass

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊：
    GET: 顯示註冊表單 (templates/auth/register.html)
    POST: 接收表單建立新使用者，重導向至 /login
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    處理使用者登出：
    清除 session 內的登入狀態，重導向至 /login
    """
    pass
