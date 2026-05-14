# 路由設計文件：生活目標追蹤+打怪系統
# 路由設計文件 (ROUTES.md)

本文件定義「生活目標追蹤 + 打怪系統」的 Flask 路由規劃、HTTP 方法與對應的 Jinja2 模板。
# 路由設計文件 — 生活目標加打怪系統

本文件定義了系統中所有頁面的 URL 路徑、對應的處理邏輯、使用的 HTTP 方法以及渲染的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
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
