# 流程圖文件 (FLOWCHART)：生活目標打怪追蹤系統 (Daily Game)

本文件將根據 PRD 的需求與系統架構，將使用者的操作路徑與系統內部的資料流視覺化。

---

## 1. 使用者流程圖 (User Flow)

此流程圖描述使用者從進入系統到操作各項功能的完整路徑。

```mermaid
flowchart TD
    Start([進入網站]) --> CheckLogin{是否已登入？}
    
    CheckLogin -->|否| LoginPage[登入 / 註冊頁]
    LoginPage --> ProcessAuth[輸入帳號密碼提交]
    ProcessAuth --> CheckAuthResult{驗證成功？}
    CheckAuthResult -->|否| LoginPage
    CheckAuthResult -->|是| Main(首頁 / 遊戲主畫面)

    CheckLogin -->|是| Main

    Main --> CheckAction{選擇功能}

    %% 任務管理流程
    CheckAction -->|管理任務| TaskList[任務管理頁面]
    TaskList --> TaskAction{選擇操作}
    TaskAction -->|新增| CreateTask[填寫新增任務表單] --> TaskList
    TaskAction -->|編輯| EditTask[修改任務內容] --> TaskList
    TaskAction -->|刪除| DeleteTask[確認刪除任務] --> TaskList

    %% 打怪核心流程
    CheckAction -->|執行任務| CompleteTask[在主畫面點擊任務「完成」]
    CompleteTask --> BattleLogic[觸發攻擊：怪物扣血]
    BattleLogic --> CalculateEXP[獲得經驗值 & 判斷是否升級/解鎖稱號]
    CalculateEXP --> Main

    %% 數據統計流程
    CheckAction -->|查看統計| StatsPage[個人成就與圖鑑頁面]
    StatsPage --> Main

    %% 登出流程
    CheckAction -->|登出| Logout([登出系統]) --> LoginPage
```

---

## 2. 系統序列圖 (Sequence Diagram)

以下以系統最核心的**「完成任務並打怪升級」**為例，展示前端瀏覽器、Flask 路由、Model 與 SQLite 資料庫之間的完整互動。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (前端)
    participant Route as Flask Route (tasks.py)
    participant TaskModel as Task Model
    participant UserModel as User Model
    participant MonsterModel as Monster Model
    participant DB as SQLite

    User->>Browser: 點擊任務的「完成」按鈕
    Browser->>Route: POST /tasks/<task_id>/complete
    
    %% 任務狀態更新
    Route->>TaskModel: 將任務標記為「已完成」
    TaskModel->>DB: UPDATE tasks SET status='completed' ...
    DB-->>TaskModel: 更新成功
    
    %% 怪物扣血邏輯
    Route->>MonsterModel: 扣除當前怪物血量
    MonsterModel->>DB: UPDATE monsters SET hp = hp - damage ...
    DB-->>MonsterModel: 更新成功
    
    %% 經驗值與等級結算
    Route->>UserModel: 增加使用者經驗值 (EXP)
    UserModel->>UserModel: 判斷是否達到升級門檻
    UserModel->>DB: UPDATE users SET exp, level, title ...
    DB-->>UserModel: 更新成功
    
    %% 回傳結果與渲染
    Route-->>Browser: 回傳成功狀態 (重新導向或傳回 JSON 數據)
    Browser->>User: 顯示攻擊動畫、血條減少與進度更新
```

---

## 3. 功能清單與路由對照表

以下整理了系統內預計實作的主要功能、對應的 URL 路徑與 HTTP 方法。

| 功能模組 | 操作描述 | URL 路徑 (建議) | HTTP 方法 |
|---|---|---|---|
| **認證 (Auth)** | 註冊新帳號 | `/register` | GET (頁面), POST (送出) |
| **認證 (Auth)** | 使用者登入 | `/login` | GET (頁面), POST (送出) |
| **認證 (Auth)** | 使用者登出 | `/logout` | GET 或 POST |
| **主畫面 (Main)** | 顯示遊戲主畫面與今日任務 | `/` | GET |
| **任務 (Tasks)** | 查看所有任務列表 | `/tasks` | GET |
| **任務 (Tasks)** | 新增任務 | `/tasks/create` | GET (表單), POST (送出) |
| **任務 (Tasks)** | 編輯任務 | `/tasks/<id>/edit` | GET (表單), POST (送出) |
| **任務 (Tasks)** | 刪除任務 | `/tasks/<id>/delete` | POST |
| **任務 (Tasks)** | 完成任務 (觸發打怪) | `/tasks/<id>/complete`| POST |
| **統計 (Stats)**| 查看個人數據、稱號與圖鑑 | `/stats` | GET |
