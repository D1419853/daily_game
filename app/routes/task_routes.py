from flask import Blueprint

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁 (任務列表與怪獸畫面)：
    1. 檢查是否登入。
    2. 檢查並執行跨日重置邏輯。
    3. 取得使用者狀態與任務列表。
    4. 渲染 templates/tasks/index.html
    """
    pass

@task_bp.route('/tasks/new', methods=['GET'])
def new_task():
    """
    顯示新增任務頁面：
    渲染 templates/tasks/new.html
    """
    pass

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    處理新增任務邏輯：
    接收表單資料，寫入資料庫，重導向至 /
    """
    pass

@task_bp.route('/tasks/<int:id>/complete', methods=['POST'])
def complete_task(id):
    """
    處理任務完成 (打怪) 邏輯：
    1. 更新指定任務的 progress。
    2. 若達成 target，標記完成並給予玩家經驗值與金幣。
    3. 重導向至 / (或回傳 JSON 供前端處理打怪動畫)
    """
    pass

@task_bp.route('/tasks/refresh', methods=['POST'])
def refresh_tasks():
    """
    處理刷新每日任務邏輯：
    清空該使用者目前的所有任務，隨機產生新任務，重導向至 /
    """
    pass
