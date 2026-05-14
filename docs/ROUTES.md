# 路由設計文件：生活目標追蹤+打怪系統

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
