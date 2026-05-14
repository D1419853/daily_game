# 系統架構設計文件：生活目標追蹤+打怪系統

## 1. 技術架構說明

本專案採用經典的 **MVC (Model-View-Controller)** 架構模式，並使用 Python 的 Flask 框架進行開發。

### 選用技術與原因
- **後端框架：Flask (Python)** - 輕量級、彈性高，適合快速原型開發，且易於學習與擴充。
- **模板引擎：Jinja2** - Flask 內建，能方便地將後端邏輯與 HTML 結合，適合此專案的伺服器渲染需求。
- **資料庫：SQLite** - 無須額外安裝資料庫伺服器，單一檔案儲存，方便開發與攜帶，對於學生專題規模而言效能足夠。

### MVC 模式說明
- **Model (模型)**：負責與 SQLite 資料庫互動，定義資料表結構（如任務、角色狀態、裝備等）與資料邏輯。
- **View (視圖)**：負責顯示介面，使用 Jinja2 渲染 HTML 頁面，將資料視覺化呈現（如血條、等級）。
- **Controller (控制器)**：在 Flask 中主要透過路由（Routes）實現，接收使用者請求（如點擊完成任務），呼叫 Model 更新資料，並決定要渲染哪個 View。

## 2. 專案資料夾結構

建議採用模組化的結構，將不同職責的程式碼分開放置：
# 系統架構設計文件 (ARCHITECTURE.md)

本文件基於 [PRD.md](file:///c:/Users/User/Desktop/daily_game/docs/PRD.md) 的需求，定義「生活目標追蹤 + 打怪系統」的技術架構與實作方案。

## 1. 技術架構說明

本系統採用 **Flask** 作為核心框架，並遵循簡化的 **MVC (Model-View-Controller)** 模式：

- **Model (模型)**：使用 SQLite 儲存資料，負責定義使用者、任務、怪物與進度等資料結構。
- **View (視圖)**：使用 Jinja2 模板引擎進行伺服器端渲染 (SSR)，負責產出 HTML 頁面並結合 CSS 與 JavaScript 進行美化與互動。
- **Controller (控制器)**：由 Flask 的路由 (Routes) 擔任，負責處理瀏覽器請求、執行業務邏輯，並決定回傳哪個 View。

### 選用技術與原因
- **Python + Flask**：輕量、易於上手，適合快速開發 MVP。
- **SQLite**：無須安裝額外伺服器，單一檔案即可運作，適合個人化與中小型專案。
- **Jinja2**：Flask 內建，能輕鬆將後端資料注入 HTML，減少前端串接 API 的複雜度。
# 系統架構設計 — 生活目標加打怪系統

## 1. 技術架構說明

本系統採用經典的 **MVC (Model-View-Controller)** 模式進行開發，以確保程式碼結構清晰且易於維護。

### 選用技術與原因
- **後端：Python + Flask**
  - 原因：Flask 是一個輕量級的 Web 框架，適合快速開發與專案原型製作，對於初學者來說學習曲線較平緩。
- **模板引擎：Jinja2**
  - 原因：Flask 內建支援，能直接在 HTML 中嵌入 Python 變數與邏輯，實現伺服器端渲染（Server-side Rendering），簡化開發流程。
- **資料庫：SQLite**
  - 原因：零設定、檔案式資料庫，無需額外安裝伺服器軟體，適合中小型專案或個人專題。
- **認證與安全性：Werkzeug (Password Hashing)**
  - 原因：Flask 內建安全工具，能輕鬆實作密碼雜湊與比對。

### MVC 模式分工
- **Model (模型)**：負責定義資料結構（如使用者資訊、任務內容、怪物數值）以及與 SQLite 資料庫的溝通。
- **View (視圖)**：由 Jinja2 模板構成，負責產出給瀏覽器呈現的 HTML 頁面與 UI 介面。
- **Controller (控制器)**：由 Flask 的路由（Routes）組成，負責接收使用者的請求、調用 Model 處理資料，並決定最後要渲染哪一個 View。

---

## 2. 專案資料夾結構

建議採用模組化的結構，方便未來擴充功能：

```text
daily_game/
├── app/
│   ├── models/           # 資料庫模型 (Model)
│   │   ├── __init__.py
│   │   ├── task.py       # 任務相關模型
│   │   └── user.py       # 使用者與角色屬性模型
│   ├── routes/           # 路由處理 (Controller)
│   │   ├── __init__.py
│   │   ├── auth.py       # 註冊登入路由
│   │   └── main.py       # 首頁、任務與打怪邏輯路由
│   ├── static/           # 靜態資源 (CSS, JS, Images)
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── game.js
│   ├── templates/        # Jinja2 HTML 模板 (View)
│   │   ├── base.html     # 共用佈局
│   │   ├── index.html    # 遊戲大廳/首頁
│   │   └── login.html    # 登入頁面
│   └── __init__.py       # Flask App 初始化
├── docs/                 # 專案文件 (PRD, Architecture)
├── instance/             # 實例資料夾 (不進入 Git)
│   └── database.db       # SQLite 資料庫檔案
├── app.py                # 應用程式進入點 (Runner)
├── config.py             # 專案設定檔
└── requirements.txt      # 依賴套件清單
```

## 3. 元件關係圖

### 系統資料流向
```mermaid
graph TD
    User((瀏覽器/使用者)) -->|點擊完成任務| Route[Flask Route / Controller]
    Route -->|呼叫更新資料| Model[Database Model]
    Model -->|更新狀態/經驗值| DB[(SQLite Database)]
    DB -->|返回更新結果| Model
    Model -->|傳回數據| Route
    Route -->|傳遞資料| View[Jinja2 Template / View]
    View -->|渲染 HTML| User
```

## 4. 關鍵設計決策

1. **伺服器渲染 (Server-Side Rendering)**：
   - 決策：不使用 React/Vue 前後端分離，直接由 Flask + Jinja2 渲染。
   - 原因：降低開發複雜度，適合單純的專題展示，且能充分利用 Flask 的整合優勢。

2. **角色屬性與任務連動**：
   - 決策：在資料庫中設計「角色屬性表」，與「任務表」連動。
   - 原因：確保每次任務完成時，經驗值與等級的變動能即時同步到使用者角色上，並保存成長進度。

3. **靜態資源優化**：
   - 決策：將遊戲相關的視覺回饋（如血條動畫）放在 `static/js` 處理。
   - 原因：減輕後端負擔，利用客戶端 JS 處理即時的視覺過渡效果，提升使用者的「遊戲感」。

4. **資料庫獨立性**：
   - 決策：使用 `instance/` 資料夾存放 SQLite 檔案。
   - 原因：這是 Flask 的最佳實踐，可以避免資料庫檔案被誤傳到 Git，同時讓開發環境設定更清晰。
│   ├── __init__.py          # 初始化 Flask App 與資料庫
│   ├── models.py            # 定義資料表模型 (User, Task, Monster)
│   ├── routes/              # 業務邏輯路由
│   │   ├── auth.py          # 註冊與登入
│   │   ├── tasks.py         # 任務管理
│   │   └── combat.py        # 戰鬥邏輯與怪物更新
│   ├── templates/           # Jinja2 HTML 模板
│   │   ├── base.html        # 共用導覽列與 Layout
│   │   ├── index.html       # 首頁 (儀表板)
│   │   ├── login.html       # 登入頁
│   │   ├── tasks.html       # 任務列表
│   │   └── combat.html      # 戰鬥畫面
│   └── static/              # 靜態資源
│       ├── css/             # CSS 樣式表
│       ├── js/              # JavaScript 互動腳本
│       └── images/          # 怪物圖片、道具圖示
├── docs/
│   ├── PRD.md               # 產品需求文件
│   └── ARCHITECTURE.md      # 系統架構文件
├── instance/
│   └── database.db          # SQLite 資料庫檔案 (運行時產生)
├── app.py                   # 專案啟動入口
├── requirements.txt         # 專案依賴套件
└── .gitignore               # 排除不必要的檔案
建議採用以下結構來組織程式碼，將不同功能的程式碼區隔開來：

```text
daily_game/
├── app/                  # 應用程式核心目錄
│   ├── __init__.py       # 初始化 Flask App 與套件設定
│   ├── models/           # 資料庫模型 (Model)
│   │   ├── __init__.py
│   │   ├── user.py       # 使用者模型
│   │   ├── task.py       # 任務模型
│   │   └── monster.py    # 怪物與角色模型
│   ├── routes/           # 路由邏輯 (Controller)
│   │   ├── __init__.py
│   │   ├── auth.py       # 註冊、登入邏輯
│   │   ├── main.py       # 首頁與打怪主邏輯
│   │   └── tasks.py      # 任務管理邏輯
│   ├── templates/        # Jinja2 HTML 模板 (View)
│   │   ├── base.html     # 共用佈局 (Navbar, Footer)
│   │   ├── index.html    # 遊戲大廳/首頁
│   │   ├── login.html    # 登入頁面
│   │   └── tasks.md      # 任務列表頁面
│   └── static/           # 靜態資源
│       ├── css/          # 樣式表 (style.css)
│       ├── js/           # 前端互動邏輯 (script.js)
│       └── images/       # 怪物圖、角色圖等素材
├── instance/             # 存放實例特定檔案 (不進入 Git 追蹤)
│   └── database.db       # SQLite 資料庫檔案
├── docs/                 # 專案文件 (PRD, Architecture)
├── .gitignore            # 排除不需上傳的檔案 (如 __pycache__)
├── app.py                # 專案啟動入口
└── requirements.txt      # 專案套件依賴清單
```

---

## 3. 元件關係圖

```mermaid
graph TD
    User((使用者)) -->|操作瀏覽器| Browser[瀏覽器]
    Browser -->|HTTP Request| Flask_Routes[Flask Routes / Controller]
    
    subgraph Backend [Flask 後端]
        Flask_Routes -->|存取資料| Models[Models / SQL]
        Models <-->|讀寫| SQLite[(SQLite Database)]
        
        Flask_Routes -->|傳遞資料| Jinja2[Jinja2 Template / View]
        Jinja2 -->|渲染頁面| HTML_Result[HTML + CSS + JS]
    end
    
    HTML_Result -->|HTTP Response| Browser
以下圖示呈現了從使用者操作到系統回應的資料流向：

```mermaid
graph LR
    User((瀏覽器)) -- 1. 請求 (GET/POST) --> Controller[Flask Route]
    Controller -- 2. 查詢/存取資料 --> Model[SQLAlchemy/Models]
    Model -- 3. SQL 指令 --> DB[(SQLite Database)]
    DB -- 4. 回傳資料 --> Model
    Model -- 5. 封裝成物件 --> Controller
    Controller -- 6. 傳遞變數 --> View[Jinja2 Template]
    View -- 7. 渲染完成 HTML --> User
```

---

## 4. 關鍵設計決策

1. **伺服器端渲染 (SSR) vs. 前後端分離**
   - **決策**：採用 SSR。
   - **原因**：考量到開發速度與複雜度，SSR 可以直接在 Python 處理好邏輯後渲染，省去建立繁瑣 API 與前端狀態管理的時間。

2. **路由模組化 (Blueprints)**
   - **決策**：將註冊登入、任務、戰鬥分開放在不同的路由檔案中。
   - **原因**：避免 `app.py` 變得過於龐大，且讓各個功能的職責清晰。

3. **戰鬥觸發機制**
   - **決策**：當使用者勾選「完成任務」時，由後端計算傷害並同步更新怪物的 HP。
   - **原因**：確保遊戲數據的正確性與安全性，防止使用者在前端直接修改傷害數值。

4. **資料庫連線管理**
   - **決策**：使用 Flask-SQLAlchemy 或直接封裝 sqlite3 操作。
   - **原因**：提供更直觀的物件導向方式操作資料，提高程式碼的可讀性。

---
*文件更新日期：2026-05-14*
1.  **採用伺服器端渲染 (SSR)**：
    由於本專案主要目標是讓初學者快速掌握全端開發，採用 Flask + Jinja2 直接渲染頁面，可以省去前端框架（如 React/Vue）與 API 通訊的複雜度，開發效率更高。
2.  **模組化路由 (Blueprints)**：
    即使是小型專案，也將認證 (`auth`)、任務 (`tasks`) 與主遊戲邏輯 (`main`) 分開撰寫，能避免 `app.py` 變得過於肥大，也方便多人協作。
3.  **基礎狀態機設計**：
    打怪機制將透過 Controller 判斷任務完成狀態，並即時更新 Model 中的角色經驗值與怪物血量，這確保了資料的一致性與遊戲邏輯的嚴謹。
4.  **靜態資源管理**：
    將圖片、CSS 與 JS 集中在 `static` 目錄，並在 `base.html` 中統籌引用，方便全站樣式的統一與資源重用。

---
