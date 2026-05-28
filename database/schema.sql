-- 1. 使用者表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 勇者角色狀態表 (與 users 連動)
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    level INTEGER DEFAULT 1,
    xp INTEGER DEFAULT 0,
    gold INTEGER DEFAULT 0,
    current_title TEXT DEFAULT '新手冒險者',
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- 3. 冒險任務表
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    difficulty INTEGER NOT NULL DEFAULT 1, -- 1 (Easy), 2 (Normal), 3 (Hard)
    status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'completed'
    duration_minutes INTEGER DEFAULT 0, -- 設定倒數計時分數
    unlock_at DATETIME, -- 解鎖可完成的具體時間
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- 4. 怪物範本表
CREATE TABLE IF NOT EXISTS monsters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    max_hp INTEGER NOT NULL,
    xp_reward INTEGER NOT NULL,
    gold_reward INTEGER NOT NULL,
    image_path TEXT NOT NULL
);

-- 5. 玩家當前遭遇怪物實體表
CREATE TABLE IF NOT EXISTS user_monster_instances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    monster_id INTEGER NOT NULL,
    current_hp INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (monster_id) REFERENCES monsters (id)
);

-- 6. 商店道具表
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    type TEXT NOT NULL, -- 'weapon', 'armor'
    bonus_stat INTEGER NOT NULL DEFAULT 0
);

-- 7. 玩家背包關聯表
CREATE TABLE IF NOT EXISTS user_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    is_equipped BOOLEAN NOT NULL DEFAULT 0,
    acquired_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
);

-- 8. 成就設定表
CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    requirement_type TEXT, -- 'task_completed'
    requirement_count INTEGER,
    reward_coins INTEGER DEFAULT 0,
    reward_title TEXT
);

-- 9. 玩家成就解鎖紀錄表
CREATE TABLE IF NOT EXISTS user_achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    achievement_id INTEGER NOT NULL,
    unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements (id) ON DELETE CASCADE
);

-- 10. 怪物擊敗紀錄表 (用於圖鑑)
CREATE TABLE IF NOT EXISTS user_defeated_monsters (
    user_id INTEGER NOT NULL,
    monster_id INTEGER NOT NULL,
    defeat_count INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, monster_id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (monster_id) REFERENCES monsters (id) ON DELETE CASCADE
);

-- 11. 等級里程碑獎勵領取紀錄表
CREATE TABLE IF NOT EXISTS user_claimed_rewards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    reward_level INTEGER NOT NULL,
    claimed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, reward_level),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- ==================== 預填初始資料 ====================

-- 預填基本怪物資料
INSERT OR IGNORE INTO monsters (id, name, max_hp, xp_reward, gold_reward, image_path) VALUES 
(1, '小史萊姆 🟢', 30, 20, 15, 'slime'),
(2, '森林野狼 🐺', 80, 50, 40, 'wolf'),
(3, '惡毒蝙蝠 🦇', 50, 30, 25, 'bat'),
(4, '哥布林強盜 👺', 120, 80, 70, 'goblin'),
(5, '遠古巨龍 🐉', 500, 300, 250, 'dragon'),
(6, '骷髏戰士 💀', 90, 60, 50, 'skeleton'),
(7, '烈焰精靈 🔥', 150, 100, 80, 'fire'),
(8, '暗影刺客 👤', 110, 75, 65, 'assassin'),
(9, '鋼鐵巨像 🤖', 250, 160, 130, 'golem'),
(10, '不死殭屍 🧟', 70, 40, 35, 'zombie'),
(11, '樹妖長老 🌳', 200, 120, 100, 'treant'),
(12, '浴火鳳凰 🐦', 300, 180, 150, 'phoenix'),
(13, '深海巨妖 🐙', 400, 250, 220, 'kraken');


-- 預填基本道具資料
INSERT OR IGNORE INTO items (id, name, description, price, type, bonus_stat) VALUES 
(1, '新手木劍 🪵', '一把散發木頭香氣的木劍，攻擊力 +5。', 30, 'weapon', 5),
(2, '精鐵長劍 🗡️', '工匠精心打造的長劍，攻擊力 +15。', 120, 'weapon', 15),
(3, '聖光巨劍 ⚔️', '附魔聖光力量的巨劍，攻擊力 +45。', 450, 'weapon', 45),
(4, '冒險皮甲 🧥', '輕便耐磨的旅行皮甲，提供基礎防護。', 50, 'armor', 0),
(5, '秘銀胸甲 🛡️', '極具防禦力的華麗胸甲。', 250, 'armor', 0);

-- 預填基本成就資料
INSERT OR IGNORE INTO achievements (id, name, description, requirement_type, requirement_count, reward_coins, reward_title) VALUES 
(1, '初出茅廬 🗡️', '擊敗第一隻怪物 (完成 1 個任務)。', 'task_completed', 1, 50, '見習勇者'),
(2, '怪物獵人 🏹', '累計擊敗 10 隻怪物 (完成 10 個任務)。', 'task_completed', 10, 200, '精銳獵人'),
(3, '屠龍勇士 👑', '累計擊敗 50 隻怪物 (完成 50 個任務)。', 'task_completed', 50, 1000, '傳說英雄');
