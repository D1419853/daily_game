# 路由設計 — 生活目標加打怪系統

本文件定義了 Flask 應用程式的所有 URL 路徑、對應的處理邏輯與 Jinja2 模板，供開發團隊分工參考。

## 1. 路由總覽表格

| 功能類別 | 功能名稱 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **帳號** | 註冊頁面 | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| **帳號** | 執行註冊 | POST | `/auth/register` | — | 建立帳號與初始化角色，完成後重導向至登入 |
| **帳號** | 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| **帳號** | 執行登入 | POST | `/auth/login` | — | 驗證身份並建立 Session，完成後重導向至首頁 |
| **帳號** | 執行登出 | POST | `/auth/logout` | — | 清除 Session 並重導向至登入頁 |
| **首頁** | 遊戲大廳 | GET | `/` | `main/index.html` | 顯示目前怪物、角色數值與任務概況 |
| **任務** | 任務清單 | GET | `/tasks` | `tasks/list.html` | 顯示該使用者所有進行中與已完成的任務 |
| **任務** | 新增任務頁面 | GET | `/tasks/new` | `tasks/form.html` | 顯示新增任務的表單 |
| **任務** | 執行新增 | POST | `/tasks/new` | — | 儲存任務資料，完成後重導向至任務清單 |
| **任務** | 編輯任務頁面 | GET | `/tasks/<id>/edit` | `tasks/form.html` | 顯示編輯任務的表單 |
| **任務** | 執行更新 | POST | `/tasks/<id>/edit` | — | 更新任務內容，完成後重導向至任務清單 |
| **任務** | 執行刪除 | POST | `/tasks/<id>/delete` | — | 移除任務，完成後重導向至任務清單 |
| **打怪** | 完成任務並攻擊 | POST | `/tasks/<id>/complete` | — | 觸發攻擊怪物、獲得獎勵邏輯，完成後重導向至首頁 |

---

## 2. 每個路由的詳細說明

### 2.1 註冊與登入
- **處理邏輯**：
  - 註冊時需呼叫 `User.create` 建立帳號，同時呼叫 `Character.create_for_user` 與 `UserMonsterInstance.create` (分配第一隻怪) 進行初始化。
  - 登入時需使用 `User.get_by_username` 並驗證密碼雜湊。
- **錯誤處理**：若帳號重複或密碼錯誤，則重新渲染表單並顯示閃退訊息 (Flash Message)。

### 2.2 任務管理
- **處理邏輯**：
  - 使用 `Task.get_all_by_user`、`Task.create` 等方法。
  - 新增與編輯共用 `tasks/form.html`。
- **輸入**：標題 (title)、描述 (description)、難度 (difficulty)。

### 2.3 完成任務與攻擊 (關鍵邏輯)
- **處理邏輯**：
  1. 呼叫 `Task.update_status` 將任務標記為已完成。
  2. 根據任務難度，呼叫 `UserMonsterInstance.damage_monster` 扣除怪物血量。
  3. 呼叫 `Character.add_rewards` 給予玩家經驗值與金幣。
  4. **檢查怪物死亡**：若怪物血量 <= 0，則呼叫 `UserMonsterInstance.create` 替換為下一隻怪物。
  5. **檢查角色升級**：若經驗值達標，更新等級並重設經驗值。

---

## 3. Jinja2 模板清單

所有模板都應位於 `app/templates/` 目錄中，並繼承 `base.html`。

- `base.html`：包含導覽列 (Navbar)、Flash 訊息顯示區域與基礎 CSS/JS 引用。
- `auth/register.html`：註冊表單。
- `auth/login.html`：登入表單。
- `main/index.html`：顯示角色狀態（HP, Level, XP, Gold）與當前怪物的圖示及血量條。
- `tasks/list.html`：任務列表表格，包含「完成」、「編輯」、「刪除」按鈕。
- `tasks/form.html`：新增與編輯任務共用的表單頁面。

---

## 4. 路由骨架程式碼

請參考 `app/routes/` 目錄下的 `auth.py`, `main.py`, 與 `tasks.py`。
