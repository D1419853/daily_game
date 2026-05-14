# 路由設計文件 (ROUTES.md)

本文件定義「生活目標追蹤 + 打怪系統」的 Flask 路由規劃、HTTP 方法與對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
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
