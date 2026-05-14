# 路由設計文件 (Routes)：打怪升級待辦清單系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁 (任務列表)** | GET | `/` | `templates/index.html` | 顯示目前使用者的任務列表與遊戲狀態概覽 |
| **註冊頁面** | GET | `/register` | `templates/login.html` | 顯示註冊表單 (通常與登入在同一頁或分開) |
| **執行註冊** | POST | `/register` | — | 接收註冊資料，建立帳號並登入，重導向至首頁 |
| **登入頁面** | GET | `/login` | `templates/login.html` | 顯示登入表單 |
| **執行登入** | POST | `/login` | — | 驗證帳號密碼，建立 Session，重導向至首頁 |
| **執行登出** | GET | `/logout` | — | 清除 Session，重導向至登入頁 |
| **新增任務** | POST | `/tasks` | — | 接收新任務標題，存入 DB，重導向至首頁 |
| **完成任務 (打怪)** | POST | `/tasks/<int:id>/complete` | — | 標記任務完成，檢查並解鎖成就，發放獎勵 |
| **刪除任務** | POST | `/tasks/<int:id>/delete` | — | 從 DB 移除任務，重導向至首頁 |
| **個人成就與背包** | GET | `/profile` | `templates/profile.html` | 顯示玩家已獲得的徽章、稱號與金幣 |
| **成就排行榜** | GET | `/leaderboard` | `templates/profile.html` | 顯示所有玩家的成就數量排名 (可與個人頁整合) |

## 2. 每個路由的詳細說明

### 2.1 驗證模組 (Auth)
- **GET /login & /register**
  - 輸出：`login.html`
- **POST /register**
  - 輸入：`username`, `email`, `password`
  - 邏輯：檢查 Email 是否重複 -> 雜湊密碼 -> 呼叫 `User.create`
  - 輸出：成功後登入並導向 `/`
- **POST /login**
  - 輸入：`email`, `password`
  - 邏輯：呼叫 `User.get_by_email` -> 驗證密碼 -> 設定 `session['user_id']`
  - 輸出：成功導向 `/`，失敗回傳錯誤訊息
- **GET /logout**
  - 邏輯：`session.clear()`
  - 輸出：導向 `/login`

### 2.2 任務模組 (Task)
- **POST /tasks**
  - 輸入：`title`
  - 邏輯：獲取目前 `user_id` -> 呼叫 `Task.create`
  - 輸出：導向 `/`
- **POST /tasks/<id>/complete**
  - 邏輯：
    1. 呼叫 `Task.mark_completed(id)`
    2. 統計該使用者已完成任務總數
    3. 檢查 `achievements` 表中是否有符合條件且尚未解鎖的成就
    4. 若有，呼叫 `Achievement.unlock` 並更新 `User` 的金幣/稱號
  - 輸出：導向 `/` 並帶有 Flash Message 提示解鎖成就
- **POST /tasks/<id>/delete**
  - 邏輯：呼叫 `Task.delete(id)`
  - 輸出：導向 `/`

### 2.3 遊戲化模組 (Index & Achievement)
- **GET /**
  - 邏輯：檢查登入狀態 -> 呼叫 `Task.get_by_user` -> 獲取使用者遊戲數值 (金幣、稱號)
  - 輸出：`index.html`
- **GET /profile**
  - 邏輯：呼叫 `Achievement.get_unlocked_by_user`
  - 輸出：`profile.html`
- **GET /leaderboard**
  - 邏輯：查詢 `users` 表並依成就數量或金幣排序
  - 輸出：`profile.html` (或獨立頁面)

## 3. Jinja2 模板清單

| 檔案路徑 | 繼承自 | 說明 |
| --- | --- | --- |
| `templates/base.html` | — | 基礎結構，包含導覽列 (顯示等級/金幣) 與靜態資源引入 |
| `templates/login.html` | `base.html` | 登入與註冊表單頁面 |
| `templates/index.html` | `base.html` | 任務列表頁面，包含「打怪」視覺化設計 |
| `templates/profile.html` | `base.html` | 成就牆與排行榜展示頁面 |

## 4. 路由骨架規劃

檔案將分為：
- `app/routes/auth.py`
- `app/routes/task.py`
- `app/routes/index.py` (包含成就與排行榜)
