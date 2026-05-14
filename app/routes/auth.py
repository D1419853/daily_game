from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.user import User
from ..models.character import Character
from ..models.monster import UserMonsterInstance

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    顯示註冊表單 (GET) 或 處理註冊邏輯 (POST)。
    註冊成功後需初始化 Character 與 UserMonsterInstance。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    顯示登入表單 (GET) 或 處理登入驗證 (POST)。
    驗證成功後將 user_id 存入 session。
    """
    pass

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    清除 session 並重導向至登入頁。
    """
    pass
