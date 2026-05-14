from flask import Blueprint, render_template, session, redirect, url_for
from ..models.character import Character
from ..models.monster import UserMonsterInstance

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    遊戲主大廳頁面。
    需取得當前登入使用者的 Character 數值與正在挑戰的 UserMonsterInstance。
    若未登入則重導向至登入頁。
    """
    pass
