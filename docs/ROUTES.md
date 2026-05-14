# 路由設計文件 (Routes)

本文件定義了「生活目標追蹤與打怪系統」中所有頁面與 API 的 URL 設計、處理邏輯與對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (任務列表) | GET | `/` | `templates/tasks/index.html` | 顯示玩家狀態、怪獸畫面與今日任務清單 |
| 登入頁面 | GET | `/login` | `templates/auth/login.html` | 顯示登入表單 |
| 處理登入 | POST | `/login` | — | 驗證帳密，設定 session，重導向至首頁 |
| 註冊頁面 | GET | `/register` | `templates/auth/register.html` | 顯示註冊表單 |
| 處理註冊 | POST | `/register` | — | 寫入資料庫建立帳號，重導向至登入頁 |
| 登出 | GET | `/logout` | — | 清除 session，重導向至登入頁 |
| 新增任務頁面 | GET | `/tasks/new` | `templates/tasks/new.html` | 顯示手動新增任務的表單 |
| 建立任務 | POST | `/tasks` | — | 接收表單資料，寫入 DB，重導向至首頁 |
| 完成任務(打怪) | POST | `/tasks/<int:id>/complete` | — | 更新任務進度，發放獎勵，重導向至首頁 (或回傳 JSON) |
| 刷新每日任務 | POST | `/tasks/refresh` | — | 清空目前的任務並重新產生，重導向至首頁 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁 (任務列表) `GET /`
- **輸入**：無（依賴 session 中的 `user_id`）。
- **處理邏輯**：
  1. 檢查是否登入，未登入則導向 `/login`。
  2. 檢查 `users.last_login_date`，若與今日不同，則觸發跨日處理（呼叫 `TaskModel.reset_daily_tasks`），並更新登入日期。
  3. 取得玩家的等級、經驗值、金幣資訊 (`UserModel.get_user_by_id`)。
  4. 取得玩家今日任務列表 (`TaskModel.get_tasks_by_user`)。
- **輸出**：渲染 `tasks/index.html`，並將玩家狀態與任務列表傳入模板。

### 2.2 登入/註冊/登出 `GET/POST /login`, `/register`, `/logout`
- **輸入**：表單欄位 (`username`, `password`)。
- **處理邏輯**：使用 `UserModel` 驗證或建立帳號，利用 Flask `session` 儲存登入狀態。
- **錯誤處理**：帳號重複或密碼錯誤時，透過 `flash` 顯示錯誤訊息並重新渲染表單頁面。

### 2.3 完成任務(打怪) `POST /tasks/<int:id>/complete`
- **輸入**：URL 參數 `id` (任務 ID)。
- **處理邏輯**：
  1. 呼叫 `TaskModel.add_progress(id)`。
  2. 若任務達到目標完成，呼叫 `UserModel.add_exp_and_coins(user_id, exp, coins)` 發放獎勵。
- **輸出**：重導向至首頁 `/`，若前端使用 AJAX，則可回傳 JSON 包含最新經驗值。

### 2.4 刷新每日任務 `POST /tasks/refresh`
- **輸入**：無。
- **處理邏輯**：
  1. 呼叫 `TaskModel.delete_all_tasks(user_id)` 清空現有任務。
  2. 從題庫或預設清單中隨機抽取並呼叫 `TaskModel.create_task` 建立新任務。
- **輸出**：透過 `flash` 顯示「每日任務已刷新！」，重導向至首頁 `/`。

---

## 3. Jinja2 模板清單

以下為本專案將實作的模板檔案清單，所有的頁面模板皆應繼承自 `base.html`：

1. **`templates/base.html`**：基礎樣板
   - 包含 HTML 骨架、匯入 CSS/JS 檔案。
   - 包含共用的頂部導覽列 (顯示玩家名稱、金幣、登出按鈕) 與 Flash 訊息顯示區塊。
2. **`templates/auth/login.html`**：登入頁面
   - 繼承 `base.html`。
   - 包含帳號密碼輸入框與送出按鈕，並提供「前往註冊」連結。
3. **`templates/auth/register.html`**：註冊頁面
   - 繼承 `base.html`。
   - 包含帳號密碼輸入框與送出按鈕。
4. **`templates/tasks/index.html`**：首頁 / 任務列表與打怪區
   - 繼承 `base.html`。
   - 區塊 1：顯示怪獸圖片與玩家目前等級、經驗值條 (Progress Bar)。
   - 區塊 2：列出今日的任務清單，每個任務旁邊有「完成 / 攻擊」按鈕。
   - 區塊 3：包含「刷新任務」與「新增任務」的按鈕。
5. **`templates/tasks/new.html`**：新增任務頁面
   - 繼承 `base.html`。
   - 包含表單讓使用者填寫任務標題與目標次數。
