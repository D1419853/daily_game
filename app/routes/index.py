from flask import Blueprint, render_template, session, redirect, url_for
from app.models.task import Task
from app.models.user import User
from app.models.achievement import Achievement

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    """首頁：顯示任務列表與遊戲狀態概覽"""
    # 檢查登入狀態
    # 載入任務與使用者數值
    pass

@index_bp.route('/profile')
def profile():
    """個人資料頁：顯示已解鎖成就與稱號"""
    # 載入成就解鎖紀錄
    pass

@index_bp.route('/leaderboard')
def leaderboard():
    """排行榜頁：依成就或金幣排序顯示玩家"""
    # 查詢並排序使用者資料
    pass
