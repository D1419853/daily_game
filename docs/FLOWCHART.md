# 流程圖文件 (FLOWCHART.md)

本文件描述「生活目標追蹤 + 打怪系統」的使用者操作路徑與系統資料流。

## 1. 使用者流程圖 (User Flow)

描述使用者從進入網站到完成任務、提升等級的完整歷程。

```mermaid
flowchart LR
    Start([開始]) --> Welcome[歡迎頁/登入頁]
    Welcome -->|登入/註冊| Dashboard[儀表板 - 任務列表]
    
    Dashboard --> Action{執行什麼操作?}
    
    Action -->|新增任務| TaskForm[填寫任務名稱與難度]
    TaskForm --> Dashboard
    
    Action -->|編輯/刪除| ModifyTask[更新任務資訊]
    ModifyTask --> Dashboard
    
    Action -->|完成任務| Battle[戰鬥觸發]
    Battle --> MonsterHP{怪物 HP <= 0?}
    
    MonsterHP -->|否| CombatFeed[顯示扣血特效與訊息]
    CombatFeed --> Dashboard
    
    MonsterHP -->|是| Victory[擊敗怪物/獲取經驗值]
    Victory --> LevelUp{經驗值足夠?}
    
    LevelUp -->|是| StatusUp[角色升級]
    StatusUp --> SpawnNew[生成下一隻怪物]
    LevelUp -->|否| SpawnNew
    
    SpawnNew --> Dashboard
```

---

## 2. 系統序列圖 (Sequence Diagram)

以「完成任務並扣除怪物血量」為例，展示後端處理流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as 業務邏輯 / Model
    participant DB as SQLite 資料庫

    User->>Browser: 點擊「完成任務」核取方塊
    Browser->>Flask: POST /tasks/complete/<id>
    
    Flask->>DB: 查詢任務詳情與目前怪物狀態
    DB-->>Flask: 回傳資料
    
    Flask->>Model: 計算傷害 (根據任務難度)
    Model-->>Flask: 傷害數值
    
    Flask->>DB: UPDATE monsters SET hp = hp - damage
    Flask->>DB: UPDATE tasks SET status = 'completed'
    
    alt 怪物被擊敗
        Flask->>Model: 計算經驗值與獎勵
        Flask->>DB: UPDATE users SET exp = exp + reward_exp
        DB-->>Flask: 成功
    end
    
    DB-->>Flask: 提交事務
    Flask-->>Browser: Redirect 或回傳 JSON 成功訊息
    Browser-->>User: 顯示戰鬥結果與動畫
```

---

## 3. 功能清單對照表

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **首頁/儀表板** | `/` | GET | 顯示目前怪物、角色狀態與任務清單 |
| **登入** | `/login` | GET/POST | 使用者驗證 |
| **註冊** | `/register` | GET/POST | 建立新帳號 |
| **新增任務** | `/tasks/add` | POST | 建立新的待辦事項 |
| **編輯任務** | `/tasks/edit/<id>` | GET/POST | 修改任務名稱或難度 |
| **刪除任務** | `/tasks/delete/<id>` | POST | 移除任務 |
| **完成任務** | `/tasks/complete/<id>` | POST | 觸發戰鬥、計算傷害 |
| **商店/獎勵** | `/shop` | GET | 查看可兌換的獎勵或道具 |

---
*文件更新日期：2026-05-14*
# 流程圖設計 — 生活目標加打怪系統

本文件視覺化了使用者的操作路徑以及系統內部的資料流向，確保功能設計符合 PRD 需求。

## 1. 使用者流程圖 (User Flow)

描述使用者進入系統後的所有操作可能路徑。

```mermaid
flowchart TD
    Start([進入網站]) --> IsLoggedIn{是否已登入？}
    IsLoggedIn -- 否 --> Auth[登入/註冊頁面]
    Auth --> LoginSuccess[登入成功]
    LoginSuccess --> MainView[遊戲主畫面 / 任務列表]
    IsLoggedIn -- 是 --> MainView

    MainView --> TaskAction{想要做什麼？}
    
    TaskAction -- 管理任務 --> TaskCRUD[新增/編輯/刪除任務]
    TaskCRUD --> MainView

    TaskAction -- 執行任務 --> CompleteTask[點擊完成任務]
    CompleteTask --> Attack[角色攻擊怪物]
    Attack --> GetXP[獲得經驗值與金幣]
    GetXP --> CheckLevel{經驗值是否全滿？}
    
    CheckLevel -- 是 --> LevelUp[等級提升 / 恢復體力]
    LevelUp --> MainView
    CheckLevel -- 否 --> MainView

    TaskAction -- 挑戰強敵 --> MonsterInfo[查看怪物狀態]
    MonsterInfo --> MainView
    
    MainView --> Logout[登出] --> Start
```

---

## 2. 系統序列圖 (Sequence Diagram) — 以「完成任務並攻擊」為例

描述當使用者完成一個任務時，資料在各元件間的流動。

```mermaid
sequenceDiagram
    actor User as 使用者 (瀏覽器)
    participant Flask as Flask Route
    participant Model as Model (Logic)
    participant DB as SQLite 資料庫

    User->>Flask: POST /tasks/1/complete
    Note over Flask: 驗證使用者身份與任務狀態
    
    Flask->>Model: 標記任務完成並計算獎勵
    Model->>DB: UPDATE tasks SET status='completed' WHERE id=1
    DB-->>Model: 更新成功
    
    Model->>DB: UPDATE characters SET xp = xp + 20 WHERE user_id=1
    DB-->>Model: 更新角色數值成功
    
    Model-->>Flask: 回傳更新後的角色與任務資料
    
    Flask-->>User: 重新導向回首頁 (顯示擊打效果與數值更新)
```

---

## 3. 功能清單與路徑對照表

根據架構設計與功能需求，規劃以下 URL 路徑：

| 功能類別 | 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **認證** | 註冊帳號 | `/auth/register` | GET, POST | 顯示註冊表單 / 儲存新帳號 |
| **認證** | 登入系統 | `/auth/login` | GET, POST | 顯示登入頁面 / 驗證身份 |
| **認證** | 登出 | `/auth/logout` | POST | 清除 Session 並登出 |
| **主遊戲** | 遊戲大廳/首頁 | `/` | GET | 顯示目前怪物、角色狀態與任務簡述 |
| **任務管理** | 任務清單頁面 | `/tasks` | GET | 檢視所有進行中與已完成的任務 |
| **任務管理** | 新增任務 | `/tasks/add` | GET, POST | 顯示新增表單 / 儲存任務資料 |
| **任務管理** | 編輯任務 | `/tasks/edit/<id>` | GET, POST | 修改現有任務內容 |
| **任務管理** | 刪除任務 | `/tasks/delete/<id>` | POST | 永久移除任務 |
| **打怪機制** | 完成任務並攻擊 | `/tasks/complete/<id>` | POST | 觸發攻擊怪物邏輯與獲取經驗值 |

---
