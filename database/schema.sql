-- 資料庫建表語法 (SQLite)

-- 1. 使用者表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    level INTEGER NOT NULL DEFAULT 1,
    experience INTEGER NOT NULL DEFAULT 0,
    gold INTEGER NOT NULL DEFAULT 0,
    current_monster_hp INTEGER NOT NULL DEFAULT 100,
    max_monster_hp INTEGER NOT NULL DEFAULT 100,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 任務表
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    category TEXT,
    status TEXT NOT NULL DEFAULT 'todo', -- todo, done
    difficulty INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. 道具表
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    type TEXT NOT NULL, -- weapon, armor
    bonus_stat INTEGER NOT NULL DEFAULT 0
);

-- 4. 使用者道具關聯表 (背包)
CREATE TABLE IF NOT EXISTS user_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    is_equipped BOOLEAN NOT NULL DEFAULT 0,
    acquired_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

-- 預填一些基本道具
INSERT INTO items (name, description, price, type, bonus_stat) VALUES 
('新手木劍', '一把基礎的木劍，增加 5 點傷害。', 50, 'weapon', 5),
('鐵劍', '鋒利的鐵劍，增加 15 點傷害。', 200, 'weapon', 15),
('布衣', '輕便的布衣，讓你在冒險中更舒適。', 30, 'armor', 2),
('皮甲', '提供基本防護的皮甲。', 150, 'armor', 8);
