# 路由設計文件 (ROUTES)：生活目標打怪追蹤系統 (Daily Game)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 首頁 (主遊戲畫面) | GET | `/` | `templates/index.html` | 顯示目前狀態、打怪主畫面與當日任務。若未登入則導向 `/login` |
| 個人統計 | GET | `/stats` | `templates/stats.html` | 顯示經驗值、等級、稱號與統計圖表 |
| 註冊頁面 | GET | `/register` | `templates/auth/register.html` | 顯示註冊表單 |
| 註冊邏輯 | POST | `/register` | — | 驗證並建立使用者，成功後重導向至 `/login` |
| 登入頁面 | GET | `/login` | `templates/auth/login.html` | 顯示登入表單 |
| 登入邏輯 | POST | `/login` | — | 驗證帳密，成功後儲存 Session，重導向至 `/` |
| 登出 | GET/POST | `/logout` | — | 清除 Session，重導向至 `/login` |
| 任務列表 | GET | `/tasks` | `templates/tasks/index.html` | 顯示所有任務列表與狀態 |
| 新增任務頁面 | GET | `/tasks/new` | `templates/tasks/new.html` | 顯示新增任務的表單 |
| 建立任務 | POST | `/tasks` | — | 接收表單，存入 DB，重導向至 `/tasks` |
| 編輯任務頁面 | GET | `/tasks/<id>/edit` | `templates/tasks/edit.html` | 顯示特定任務的編輯表單 |
| 更新任務 | POST | `/tasks/<id>/update` | — | 接收表單更新 DB，重導向至 `/tasks` |
| 刪除任務 | POST | `/tasks/<id>/delete` | — | 從 DB 刪除任務，重導向至 `/tasks` |
| 完成任務(打怪) | POST | `/tasks/<id>/complete` | — | 標記任務完成，扣除怪物血量並給予經驗值，重導向至 `/` |

## 2. 每個路由的詳細說明

### Auth 路由 (`auth.py`)
- **GET /register**
  - 處理邏輯：渲染註冊頁面。
- **POST /register**
  - 輸入：`username`, `password`, `confirm_password`。
  - 處理邏輯：檢查兩次密碼是否相符，檢查帳號是否已存在。成功則呼叫 `User.create()`，並 flash 成功訊息。
  - 輸出：重導向至 `/login`。若失敗則重新渲染 `/register` 並帶有錯誤訊息。
- **GET /login**
  - 處理邏輯：渲染登入頁面。
- **POST /login**
  - 輸入：`username`, `password`。
  - 處理邏輯：呼叫 `User.get_by_username()`，比對密碼。成功則將 user_id 寫入 session。
  - 輸出：重導向至 `/`。若失敗則 flash 錯誤訊息並重新渲染 `/login`。
- **GET /logout**
  - 處理邏輯：清除 session 中的 user_id 登入資訊。
  - 輸出：重導向至 `/login`。

### Main 路由 (`main.py`)
- **GET /**
  - 處理邏輯：檢查 session 是否有登入，若無則導向 `/login`。若有登入，取得當前使用者資料 (`User.get_by_id()`)、目前的怪物資料 (`Monster.get_active_monster()`) 以及未完成的任務 (`Task.get_by_user()`)。
  - 輸出：渲染 `index.html`。
- **GET /stats**
  - 處理邏輯：取得當前使用者的完整資訊與過去紀錄。
  - 輸出：渲染 `stats.html`。

### Tasks 路由 (`tasks.py`)
- **GET /tasks**
  - 處理邏輯：呼叫 `Task.get_by_user()` 取得使用者的所有任務。
  - 輸出：渲染 `tasks/index.html`。
- **GET /tasks/new**
  - 處理邏輯：渲染新增表單。
- **POST /tasks**
  - 輸入：`title`, `description`。
  - 處理邏輯：呼叫 `Task.create()`。
  - 輸出：重導向至 `/tasks`。
- **GET /tasks/<id>/edit**
  - 處理邏輯：透過 `Task.get_by_id()` 取得該筆任務資料。如果任務不存在或非該使用者擁有，則回傳 404 或 403。
  - 輸出：渲染 `tasks/edit.html`。
- **POST /tasks/<id>/update**
  - 輸入：`title`, `description`。
  - 處理邏輯：呼叫 `Task.update()`。
  - 輸出：重導向至 `/tasks`。
- **POST /tasks/<id>/delete**
  - 處理邏輯：呼叫 `Task.delete()`。
  - 輸出：重導向至 `/tasks`。
- **POST /tasks/<id>/complete**
  - 處理邏輯：呼叫 `Task.complete()`，接著呼叫 `Monster.take_damage()` 扣除血量，再呼叫 `User.update_stats()` 給予經驗值。
  - 輸出：重導向回首頁 `/` 並閃現 (flash) 打怪成功與經驗值提升的訊息。

## 3. Jinja2 模板清單

- `templates/base.html`：包含 `<head>`、Navbar、Footer 等全站共用元件。所有頁面都會繼承此檔案。
- `templates/auth/login.html`：登入頁面，繼承 `base.html`。
- `templates/auth/register.html`：註冊頁面，繼承 `base.html`。
- `templates/index.html`：首頁（遊戲主畫面），顯示目前面對的怪物血條與今日任務清單，繼承 `base.html`。
- `templates/stats.html`：個人數據統計頁面，繼承 `base.html`。
- `templates/tasks/index.html`：所有歷史任務與清單，繼承 `base.html`。
- `templates/tasks/new.html`：新增任務表單，繼承 `base.html`。
- `templates/tasks/edit.html`：編輯任務表單，繼承 `base.html`。
