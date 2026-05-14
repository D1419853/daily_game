# 路由設計文件 (Routes)

本文件定義了「生活目標追蹤與打怪系統」中所有頁面與 API 的 URL 設計、處理邏輯與對應的 Jinja2 模板。
# 路由設計文件 (Routes)：打怪升級待辦清單系統
# 路由設計文件 (ROUTES)：生活目標打怪追蹤系統 (Daily Game)
# 路由設計文件：生活目標追蹤+打怪系統
# 路由設計文件 (ROUTES.md)

本文件定義「生活目標追蹤 + 打怪系統」的 Flask 路由規劃、HTTP 方法與對應的 Jinja2 模板。
# 路由設計文件 — 生活目標加打怪系統

本文件定義了系統中所有頁面的 URL 路徑、對應的處理邏輯、使用的 HTTP 方法以及渲染的 Jinja2 模板。

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
| :--- | :--- | :--- | :--- | :--- |
| **首頁與任務** | | | | |
| 首頁 (任務列表) | GET | `/` | `index.html` | 顯示所有任務與角色/怪物狀態 |
| 新增任務頁面 | GET | `/task/new` | `task_form.html` | 顯示新增任務表單 |
| 建立任務 | POST | `/task/add` | — | 接收表單並存入資料庫 |
| 編輯任務頁面 | GET | `/task/edit/<id>` | `task_form.html` | 顯示編輯任務表單 |
| 更新任務 | POST | `/task/update/<id>` | — | 更新資料庫中的任務資訊 |
| 刪除任務 | POST | `/task/delete/<id>` | — | 刪除任務後重導向回首頁 |
| 完成任務 (打怪) | POST | `/task/complete/<id>` | — | 標記完成、計算傷害/經驗值並更新狀態 |
| **身分驗證** | | | | |
| 註冊頁面 | GET | `/register` | `register.html` | 顯示註冊表單 |
| 執行註冊 | POST | `/register` | — | 建立帳號並重導向 |
| 登入頁面 | GET | `/login` | `login.html` | 顯示登入表單 |
| 執行登入 | POST | `/login` | — | 驗證身分並建立 Session |
| 登出 | GET | `/logout` | — | 清除 Session 並重導向 |
| **商城與統計** | | | | |
| 商城頁面 | GET | `/shop` | `shop.html` | 顯示可購買道具與目前金幣 |
| 購買道具 | POST | `/shop/buy/<id>` | — | 扣除金幣並加入使用者背包 |
| 統計頁面 | GET | `/stats` | `stats.html` | 顯示任務達成率圖表 |

## 2. 每個路由的詳細說明

### 首頁 (GET /)
- **輸入**：無（從 Session 取得 user_id）。
- **處理邏輯**：
    1. 呼叫 `TaskModel.get_all_by_user` 抓取任務。
    2. 呼叫 `UserModel.get_by_id` 抓取角色與怪物狀態。
- **輸出**：渲染 `index.html`。

### 完成任務 (POST /task/complete/<id>)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：
    1. 呼叫 `TaskModel.update_status` 將任務改為 `done`。
    2. 根據任務難度計算 EXP, Gold 與傷害。
    3. 呼叫 `UserModel.update_stats` 更新數值。
- **輸出**：重導向回 `/`。

### 購買道具 (POST /shop/buy/<id>)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：
    1. 查詢道具價格。
    2. 檢查使用者金幣餘額。
    3. 扣除金幣並呼叫 `ItemModel.add_to_user`。
- **輸出**：重導向回 `/shop`。

## 3. Jinja2 模板清單

| 檔案名稱 | 說明 | 繼承模板 |
| :--- | :--- | :--- |
| `base.html` | 導覽列、頁尾、共用 CSS/JS 引入 | — |
| `index.html` | 首頁：任務清單、角色/怪物狀態展示 | `base.html` |
| `task_form.html` | 新增與編輯任務共用的表單頁面 | `base.html` |
| `login.html` | 使用者登入頁面 | `base.html` |
| `register.html` | 使用者註冊頁面 | `base.html` |
| `shop.html` | 道具商店頁面 | `base.html` |
| `stats.html` | 數據統計展示頁面 | `base.html` |

## 4. 路由骨架程式碼規劃

- `app/routes/auth.py`：身分驗證相關。
- `app/routes/main.py`：主要功能與任務管理。
| **首頁 (儀表板)** | GET | `/` | `index.html` | 顯示角色狀態、目前怪物與任務清單 |
| **登入頁面** | GET | `/login` | `login.html` | 顯示登入表單 |
| **執行登入** | POST | `/login` | — | 驗證身分並導向首頁 |
| **註冊頁面** | GET | `/register` | `register.html` | 顯示註冊表單 |
| **執行註冊** | POST | `/register` | — | 建立帳號並導向登入頁 |
| **登出** | GET | `/logout` | — | 清除 Session 並導向登入頁 |
| **新增任務頁面** | GET | `/tasks/new` | `tasks_form.html` | 顯示新增任務表單 |
| **建立任務** | POST | `/tasks/add` | — | 儲存任務並導向首頁 |
| **編輯任務頁面** | GET | `/tasks/edit/<int:id>` | `tasks_form.html` | 顯示編輯表單 |
| **更新任務** | POST | `/tasks/update/<int:id>` | — | 更新任務並導向首頁 |
| **刪除任務** | POST | `/tasks/delete/<int:id>` | — | 刪除任務並導向首頁 |
| **完成任務 (戰鬥)** | POST | `/tasks/complete/<int:id>` | — | 計算傷害、更新怪物與經驗值 |
| **商店頁面** | GET | `/shop` | `shop.html` | 顯示獎勵兌換清單 |

---

## 2. 每個路由的詳細說明

### 2.1 任務管理 (tasks.py)
- **建立任務**:
  - 輸入：`title`, `difficulty`
  - 邏輯：呼叫 `Task.create()`
  - 輸出：重導向至 `/`
- **完成任務**:
  - 輸入：任務 ID
  - 邏輯：
    1. 呼叫 `Task.complete()`
    2. 根據任務難度，呼叫 `Monster.take_damage()`
    3. 若怪物死亡，呼叫 `User.update_progress()` 並生成新怪物
  - 輸出：重導向至 `/` 並帶有 Flash 訊息

### 2.2 身份驗證 (auth.py)
- **登入**:
  - 邏輯：檢查 `password_hash` 是否符合。
  - 輸出：將 `user_id` 存入 Flask Session。
| **首頁 (遊戲大廳)** | GET | `/` | `index.html` | 顯示目前怪物狀態、角色資訊與任務摘要 |
| **註冊頁面** | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| **執行註冊** | POST | `/auth/register` | — | 建立帳號與初始角色，重導向至登入 |
| **登入頁面** | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| **執行登入** | POST | `/auth/login` | — | 驗證帳號，設定 Session，重導向至首頁 |
| **執行登出** | POST | `/auth/logout` | — | 清除 Session，重導向至登入頁面 |
| **任務列表** | GET | `/tasks` | `tasks/list.html` | 顯示使用者所有進行中與已完成的任務 |
| **新增任務頁面** | GET | `/tasks/new` | `tasks/new.html` | 顯示新增任務表單 |
| **執行新增任務** | POST | `/tasks` | — | 接收資料並存入 DB，重導向至列表頁 |
| **編輯任務頁面** | GET | `/tasks/<id>/edit` | `tasks/edit.html` | 顯示編輯表單 |
| **執行更新任務** | POST | `/tasks/<id>/update` | — | 更新資料，重導向至列表頁 |
| **執行刪除任務** | POST | `/tasks/<id>/delete` | — | 刪除任務，重導向至列表頁 |
| **完成任務並攻擊** | POST | `/tasks/<id>/complete` | — | 標記任務完成，扣除怪物血量並發放獎勵 |

---

## 2. 路由詳細說明

### 2.1 首頁 (Index)
- **輸入**：無
- **處理邏輯**：
  1. 檢查 Session 是否已登入。
  2. 呼叫 `Character.get_by_user_id` 取得角色數值。
  3. 呼叫 `UserMonsterInstance.get_current_for_user` 取得目前遭遇的怪物。
- **輸出**：渲染 `index.html`。
- **錯誤處理**：未登入時重導向至 `/auth/login`。

### 2.2 任務管理 (Tasks)
- **輸入**：表單資料 (title, description, difficulty)
- **處理邏輯**：
  - 新增：呼叫 `Task.create`。
  - 刪除：呼叫 `Task.delete` (需檢查權限)。
  - 完成並攻擊：
    1. 呼叫 `Task.update_status`。
    2. 根據任務難度計算傷害量。
    3. 呼叫 `UserMonsterInstance.damage_monster`。
    4. 呼叫 `Character.add_rewards` 發放經驗值與金幣。
- **輸出**：大部分重導向至 `/tasks` 或 `/`。

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
所有模板皆存放在 `app/templates/` 目錄下：

| 檔案名稱 | 繼承對象 | 內容說明 |
| :--- | :--- | :--- |
| `base.html` | — | 包含導覽列 (Navbar)、Flash 訊息與共用 CSS/JS 引用。 |
| `index.html` | `base.html` | 主介面：左側顯示怪物血量與圖片，右側顯示任務清單。 |
| `login.html` | `base.html` | 登入表單。 |
| `register.html` | `base.html` | 註冊表單。 |
| `tasks_form.html`| `base.html` | 共用的任務新增/編輯表單。 |
| `shop.html` | `base.html` | 獎勵兌換介面。 |

---

## 4. 路由骨架程式碼規劃

我們將使用 Flask Blueprint 來組織路由：
- `app/routes/auth.py`：處理登入、註冊、登出。
- `app/routes/tasks.py`：處理任務 CRUD。
- `app/routes/combat.py`：處理戰鬥邏輯與商店。

---
*文件更新日期：2026-05-14*
- `base.html`：基礎佈局，包含導覽列與靜態資源引用。
- `index.html`：繼承 `base.html`，遊戲核心介面。
- `auth/login.html`：登入介面。
- `auth/register.html`：註冊介面。
- `tasks/list.html`：任務管理清單。
- `tasks/new.html`：新增任務表單頁。
- `tasks/edit.html`：編輯任務表單頁。

---

## 4. 路由骨架程式碼

請參考 `app/routes/` 目錄下的：
- `main.py`
- `auth.py`
- `tasks.py`
