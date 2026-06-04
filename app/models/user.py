from app.models.database import get_db_connection
import sqlite3

class User:
    @staticmethod
    def create(username, password_hash):
        """建立新使用者並同時初始化勇者角色"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # 1. 插入使用者帳號
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            user_id = cursor.lastrowid
            
            # 2. 初始化勇者角色屬性
            import datetime
            today_str = datetime.date.today().isoformat()
            cursor.execute(
                "INSERT INTO characters (user_id, level, xp, gold, current_title, current_hp, max_hp, daily_goal, tasks_done_today, last_active_date) VALUES (?, 1, 0, 0, '新手冒險者', 100, 100, 3, 0, ?)",
                (user_id, today_str)
            )
            
            conn.commit()
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """取得單一勇者及其角色狀態"""
        conn = get_db_connection()
        try:
            query = """
                SELECT u.id, u.username, c.level, c.xp, c.gold, c.current_title, u.created_at,
                       c.current_hp, c.max_hp, c.daily_goal, c.tasks_done_today, c.last_active_date
                FROM users u
                JOIN characters c ON u.id = c.user_id
                WHERE u.id = ?
            """
            user = conn.execute(query, (user_id,)).fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_username(username):
        """僅取得帳密資訊以供登入驗證"""
        conn = get_db_connection()
        try:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得所有勇者列表 (用於排行榜)"""
        conn = get_db_connection()
        try:
            query = """
                SELECT u.id, u.username, c.level, c.xp, c.gold, c.current_title
                FROM users u
                JOIN characters c ON u.id = c.user_id
                ORDER BY c.gold DESC, c.level DESC
            """
            users = conn.execute(query).fetchall()
            return [dict(u) for u in users]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update_character(user_id, gold=None, xp=None, level=None, current_title=None, current_hp=None, tasks_done_today=None):
        """彈性更新勇者屬性"""
        conn = get_db_connection()
        try:
            updates = []
            values = []
            if gold is not None:
                updates.append("gold = ?")
                values.append(gold)
            if xp is not None:
                updates.append("xp = ?")
                values.append(xp)
            if level is not None:
                updates.append("level = ?")
                values.append(level)
            if current_title is not None:
                updates.append("current_title = ?")
                values.append(current_title)
            if current_hp is not None:
                updates.append("current_hp = ?")
                values.append(current_hp)
            if tasks_done_today is not None:
                updates.append("tasks_done_today = ?")
                values.append(tasks_done_today)
                
            if not updates:
                return False
                
            values.append(user_id)
            query = f"UPDATE characters SET {', '.join(updates)} WHERE user_id = ?"
            conn.execute(query, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating character: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def add_rewards(user_id, xp_gain, gold_gain):
        """給予經驗值與金幣獎勵，並處理升級邏輯"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # 1. 取得當前屬性
            cursor.execute("SELECT level, xp, gold FROM characters WHERE user_id = ?", (user_id,))
            char = cursor.fetchone()
            if not char:
                return False
                
            current_level = char['level']
            current_xp = char['xp']
            current_gold = char['gold']
            
            # 2. 計算新數值
            new_xp = current_xp + xp_gain
            new_gold = current_gold + gold_gain
            new_level = current_level
            
            # 3. 升級邏輯：每級所需經驗值為 level * 100
            xp_required = new_level * 100
            leveled_up = False
            while new_xp >= xp_required:
                new_xp -= xp_required
                new_level += 1
                xp_required = new_level * 100
                leveled_up = True
                
            # 4. 更新資料庫
            cursor.execute(
                "UPDATE characters SET level = ?, xp = ?, gold = ? WHERE user_id = ?",
                (new_level, new_xp, new_gold, user_id)
            )
            conn.commit()
            return {"leveled_up": leveled_up, "new_level": new_level, "xp_gain": xp_gain, "gold_gain": gold_gain}
        except Exception as e:
            print(f"Error adding rewards: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    LEVEL_REWARDS_CONFIG = {
        10: {"gold": 500, "title": "初階冒險大師 🏅"},
        20: {"gold": 1500, "title": "幻獸終結者 ⚔️"},
        30: {"gold": 5000, "title": "聖光守護者 🌟"},
        40: {"gold": 12000, "title": "元素主宰者 🔮"},
        50: {"gold": 30000, "title": "弒神之刃 👑"}
    }

    @staticmethod
    def get_claimed_rewards(user_id):
        """取得使用者已領取的等級獎勵清單"""
        conn = get_db_connection()
        try:
            rows = conn.execute(
                "SELECT reward_level FROM user_claimed_rewards WHERE user_id = ?",
                (user_id,)
            ).fetchall()
            return [r['reward_level'] for r in rows]
        except Exception as e:
            print(f"Error getting claimed rewards: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def claim_level_reward(user_id, level):
        """領取等級獎勵"""
        if level not in User.LEVEL_REWARDS_CONFIG:
            return False, "無效的獎勵等級"

        reward = User.LEVEL_REWARDS_CONFIG[level]
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # 1. 檢查玩家目前等級
            cursor.execute("SELECT level, gold, current_title FROM characters WHERE user_id = ?", (user_id,))
            char = cursor.fetchone()
            if not char:
                return False, "找不到角色資料"

            if char['level'] < level:
                return False, f"等級不足！需要達到 LV.{level}"

            # 2. 檢查是否已經領過
            cursor.execute(
                "SELECT id FROM user_claimed_rewards WHERE user_id = ? AND reward_level = ?",
                (user_id, level)
            )
            if cursor.fetchone():
                return False, "該等級獎勵已領取過"

            # 3. 發放獎勵
            new_gold = char['gold'] + reward['gold']
            new_title = reward['title']

            cursor.execute(
                "UPDATE characters SET gold = ?, current_title = ? WHERE user_id = ?",
                (new_gold, new_title, user_id)
            )
            
            # 4. 寫入領取紀錄
            cursor.execute(
                "INSERT INTO user_claimed_rewards (user_id, reward_level) VALUES (?, ?)",
                (user_id, level)
            )

            conn.commit()
            return True, f"成功領取 LV.{level} 獎勵！獲得 🪙 {reward['gold']} 金幣並獲得新稱號「{reward['title']}」！"
        except Exception as e:
            print(f"Error claiming level reward: {e}")
            conn.rollback()
            return False, "系統錯誤，請稍後再試"
        finally:
            conn.close()

    @staticmethod
    def process_daily_check(user_id):
        """處理每日登入檢查（判定前一天任務是否達標，若未達標則反傷）"""
        conn = get_db_connection()
        import datetime
        today_str = datetime.date.today().isoformat()
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT current_hp, daily_goal, tasks_done_today, last_active_date, gold FROM characters WHERE user_id = ?", (user_id,))
            char = cursor.fetchone()
            if not char:
                return None
                
            last_date = char['last_active_date']
            if last_date and last_date != today_str:
                # 跨日結算
                damage_taken = 0
                new_hp = char['current_hp']
                new_gold = char['gold']
                msg = None
                
                if char['tasks_done_today'] < char['daily_goal']:
                    # 未達標，受到 30 反傷
                    damage_taken = 30
                    new_hp -= damage_taken
                    msg = "⚠️ 您昨天未完成每日目標，遭到怪物反傷失去了 30 點生命值！"
                    
                    if new_hp <= 0:
                        # 死亡懲罰：扣除一半金幣，血量回滿
                        new_hp = 100
                        new_gold = int(new_gold / 2)
                        msg += " 💀 您的血量歸零，被救回了城鎮... 但遺失了一半的金幣！"
                        
                # 更新今日狀態
                cursor.execute(
                    "UPDATE characters SET last_active_date = ?, tasks_done_today = 0, current_hp = ?, gold = ? WHERE user_id = ?",
                    (today_str, new_hp, new_gold, user_id)
                )
                conn.commit()
                return msg
                
            return None
        except Exception as e:
            print(f"Error processing daily check: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
