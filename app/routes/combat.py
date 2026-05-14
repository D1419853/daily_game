from flask import Blueprint, render_template, redirect, url_for, session

combat_bp = Blueprint('combat', __name__)

@combat_bp.route('/')
def index():
    """
    儀表板首頁。
    顯示：
    1. 角色資訊 (等級, EXP, 金幣)
    2. 目前挑戰的怪物資訊
    3. 使用者的任務清單
    """
    pass

@combat_bp.route('/shop')
def shop():
    """
    商店頁面。
    顯示可用金幣兌換的獎勵。
    """
    pass
