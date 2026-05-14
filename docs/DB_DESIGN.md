# 資料庫設計文件 (DB_DESIGN.md)

本文件定義「生活目標追蹤 + 打怪系統」的資料庫結構。我們採用 SQLite 作為資料庫系統。

## 1. ER 圖 (Entity-Relationship Diagram)

```mermaid
erDiagram
    USER ||--o{ TASK : "擁有"
    USER ||--o{ MONSTER : "正在挑戰"
    USER ||--o{ COMBAT_LOG : "記錄"
# 資料庫設計 — 生活目標加打怪系統

本文件定義了系統的資料模型、表結構以及 Python 中的 Model 實作方式。

## 1. ER 圖 (Entity Relationship Diagram)

```mermaid
erDiagram
    USER ||--|| CHARACTER : "擁有"
    USER ||--o{ TASK : "建立"
    USER ||--o{ USER_MONSTER_INSTANCE : "目前遭遇"
    MONSTER ||--o{ USER_MONSTER_INSTANCE : "範本"

    USER {
        int id PK
        string username
        string password_hash
        int level
        int exp
        int gold
        datetime created_at
    }

    CHARACTER {
        int id PK
        int user_id FK
        int level
        int xp
        int gold
        int hp
        int max_hp
    }

    TASK {
        int id PK
        int user_id FK
        string title
        int difficulty "1:易, 2:中, 3:難"
        string status "pending / completed"
        string description
        int difficulty
        boolean is_completed
        datetime created_at
    }

    MONSTER {
        int id PK
        int user_id FK
        string name
        string monster_type
        int max_hp
        int current_hp
        string image_url
        boolean is_alive
        datetime created_at
    }

    COMBAT_LOG {
        int id PK
        int user_id FK
        string action_text
        int damage_dealt
        datetime created_at
        string name
        int max_hp
        int xp_reward
        int gold_reward
        string image_path
    }

    USER_MONSTER_INSTANCE {
        int id PK
        int user_id FK
        int monster_id FK
        int current_hp
    }
```

---

## 2. 資料表詳細說明

### USER (使用者)
| 欄位名 | 型別 | 說明 | 必填 |
| :--- | :--- | :--- | :--- |
| id | INTEGER | 流水號 (PK) | 是 |
| username | TEXT | 帳號名稱 (Unique) | 是 |
| password_hash | TEXT | 加密後的密碼 | 是 |
| level | INTEGER | 目前等級 (預設 1) | 是 |
| exp | INTEGER | 目前經驗值 | 是 |
| gold | INTEGER | 持有金幣 | 是 |
| created_at | DATETIME | 註冊時間 | 是 |

### TASK (任務)
| 欄位名 | 型別 | 說明 | 必填 |
| :--- | :--- | :--- | :--- |
| id | INTEGER | 流水號 (PK) | 是 |
| user_id | INTEGER | 關聯使用者 (FK) | 是 |
| title | TEXT | 任務標題 | 是 |
| difficulty | INTEGER | 難度 (1: 10傷, 2: 30傷, 3: 50傷) | 是 |
| status | TEXT | 狀態 (pending/completed) | 是 |
| created_at | DATETIME | 建立時間 | 是 |

### MONSTER (怪物)
| 欄位名 | 型別 | 說明 | 必填 |
| :--- | :--- | :--- | :--- |
| id | INTEGER | 流水號 (PK) | 是 |
| user_id | INTEGER | 關聯使用者 (正在打這隻怪的人) | 是 |
| name | TEXT | 怪物名稱 | 是 |
| monster_type | TEXT | 怪物種類 (slime, dragon, etc.) | 是 |
| max_hp | INTEGER | 最大血量 | 是 |
| current_hp | INTEGER | 目前血量 | 是 |
| image_url | TEXT | 怪物圖片路徑 | 否 |
| is_alive | BOOLEAN | 是否存活 (1:活, 0:死) | 是 |
| created_at | DATETIME | 出現時間 | 是 |

---

## 3. SQL 建表語法 (database/schema.sql)

```sql
-- 使用者表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    level INTEGER DEFAULT 1,
    exp INTEGER DEFAULT 0,
    gold INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 任務表
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    difficulty INTEGER DEFAULT 1,
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- 怪物表
CREATE TABLE IF NOT EXISTS monsters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    monster_type TEXT NOT NULL,
    max_hp INTEGER NOT NULL,
    current_hp INTEGER NOT NULL,
    image_url TEXT,
    is_alive INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- 戰鬥日誌
CREATE TABLE IF NOT EXISTS combat_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    action_text TEXT NOT NULL,
    damage_dealt INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

---
*文件更新日期：2026-05-14*
### 2.1 users (使用者)
| 欄位名 | 型別 | 說明 | 必填 |
| :--- | :--- | :--- | :--- |
| id | INTEGER | Primary Key, 自動遞增 | 是 |
| username | TEXT | 使用者名稱 (唯一) | 是 |
| password_hash | TEXT | 加密後的密碼 | 是 |

### 2.2 characters (角色數值)
| 欄位名 | 型別 | 說明 | 必填 |
| :--- | :--- | :--- | :--- |
| id | INTEGER | Primary Key, 自動遞增 | 是 |
| user_id | INTEGER | Foreign Key (users.id) | 是 |
| level | INTEGER | 目前等級 (預設 1) | 是 |
| xp | INTEGER | 目前經驗值 | 是 |
| gold | INTEGER | 持有金幣 | 是 |
| hp | INTEGER | 目前血量 | 是 |
| max_hp | INTEGER | 血量上限 | 是 |

### 2.3 tasks (任務清單)
| 欄位名 | 型別 | 說明 | 必填 |
| :--- | :--- | :--- | :--- |
| id | INTEGER | Primary Key, 自動遞增 | 是 |
| user_id | INTEGER | Foreign Key (users.id) | 是 |
| title | TEXT | 任務標題 | 是 |
| description | TEXT | 任務細節說明 | 否 |
| difficulty | INTEGER | 難度 (1:容易, 2:普通, 3:困難) | 是 |
| is_completed | BOOLEAN | 是否已完成 (0:否, 1:是) | 是 |
| created_at | DATETIME | 建立時間 | 是 |

### 2.4 monsters (怪物範本庫)
| 欄位名 | 型別 | 說明 | 必填 |
| :--- | :--- | :--- | :--- |
| id | INTEGER | Primary Key, 自動遞增 | 是 |
| name | TEXT | 怪物名稱 | 是 |
| max_hp | INTEGER | 怪物血量上限 | 是 |
| xp_reward | INTEGER | 擊敗後的經驗值獎勵 | 是 |
| gold_reward | INTEGER | 擊敗後的金幣獎勵 | 是 |
| image_path | TEXT | 怪物圖片的路徑 | 是 |

### 2.5 user_monster_instances (使用者當前遭遇怪物)
| 欄位名 | 型別 | 說明 | 必填 |
| :--- | :--- | :--- | :--- |
| id | INTEGER | Primary Key, 自動遞增 | 是 |
| user_id | INTEGER | Foreign Key (users.id) | 是 |
| monster_id | INTEGER | Foreign Key (monsters.id) | 是 |
| current_hp | INTEGER | 該怪物剩餘血量 | 是 |

---

## 3. SQL 建表語法

請參考 `database/schema.sql` 檔案。

---

## 4. Python Model 實作

Model 將採用 `sqlite3` 套件進行實作，每個 Model 類別將封裝 CRUD (Create, Read, Update, Delete) 操作。
檔案位置：`app/models/`
