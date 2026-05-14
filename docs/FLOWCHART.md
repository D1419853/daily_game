# 流程圖文件：生活目標追蹤+打怪系統

## 1. 使用者流程圖 (User Flow)

此圖描述使用者進入網站後的操作路徑，涵蓋核心的任務管理與打怪升級流程。

```mermaid
flowchart LR
    Start([進入網站]) --> Login[登入/註冊頁面]
    Login --> Home[首頁 - 任務列表與角色狀態]
    
    Home --> Action{選擇操作}
    
    Action -->|新增任務| CreateTask[填寫任務名稱/類別]
    CreateTask --> TaskList[回首頁列表]
    
    Action -->|完成任務| CompleteTask[點擊打勾完成]
    CompleteTask --> Animation[觸發打怪動畫與經驗值增加]
    Animation --> LevelUp{經驗值滿?}
    LevelUp -->|是| LevelEffect[角色升級效果]
    LevelUp -->|否| Home
    LevelEffect --> Home
    
    Action -->|商城/裝備| Shop[進入商城頁面]
    Shop --> Buy[消耗金幣購買裝備]
    Buy --> Equip[自動穿戴並提升數值]
    Equip --> Home
    
    Action -->|查看統計| Statistics[查看數據圖表]
    Statistics --> Home
```

## 2. 系統序列圖 (Sequence Diagram)

此圖以「完成任務並打怪」為例，展示資料如何在各元件間流動。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (JS/Jinja2)
    participant Flask as Flask Route (Controller)
    participant Model as Database Model
    participant DB as SQLite

    User->>Browser: 點擊「完成任務」按鈕
    Browser->>Flask: POST /complete_task/<id>
    
    Flask->>Model: 查詢該任務與角色目前狀態
    Model->>DB: SELECT * FROM tasks/users
    DB-->>Model: 返回數據
    
    Flask->>Model: 計算傷害與經驗值增量
    Model->>DB: UPDATE tasks (status=done)
    Model->>DB: UPDATE users (exp, gold, monster_hp)
    DB-->>Model: 更新成功
    
    Flask-->>Browser: 返回更新後的 JSON 資料 (exp, hp, status)
    
    Browser->>Browser: 執行前端動畫效果 (血條減少、進度條增長)
    Browser-->>User: 顯示任務完成與怪物受傷回饋
```

## 3. 功能清單對照表

以下為本系統規劃的主要功能及其對應的路徑：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| 首頁 / 任務列表 | `/` | GET | 顯示所有任務、角色血條、經驗值與怪物狀態 |
| 使用者註冊 | `/register` | GET/POST | 新增使用者帳號 |
| 使用者登入 | `/login` | GET/POST | 驗證身份並登入 |
| 新增任務 | `/task/add` | POST | 建立新的生活目標 |
| 完成任務 | `/task/complete/<id>` | POST | 標記任務完成並觸發打怪邏輯 |
| 編輯/刪除任務 | `/task/edit/<id>` / `/task/delete/<id>` | POST | 管理現有任務 |
| 商城頁面 | `/shop` | GET | 顯示可購買的裝備或道具 |
| 購買裝備 | `/shop/buy/<item_id>` | POST | 消耗金幣購買並穿戴裝備 |
| 數據統計 | `/stats` | GET | 顯示週/月達成率圖表 |

---

這些流程圖與表格能幫助開發團隊更清楚地理解系統的運作邏輯，避免在實作路由與資料庫邏輯時出現遺漏。
