from app.models.database import get_db_connection

class Item:
    @staticmethod
    def get_all():
        """取得商店所有商品"""
        conn = get_db_connection()
        try:
            items = conn.execute("SELECT * FROM items").fetchall()
            return [dict(i) for i in items]
        except Exception as e:
            print(f"Error getting items: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(item_id):
        """依 ID 取得商品資訊"""
        conn = get_db_connection()
        try:
            item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
            return dict(item) if item else None
        except Exception as e:
            print(f"Error getting item by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_user_items(user_id):
        """取得玩家背包裡所有的道具及穿戴狀態"""
        conn = get_db_connection()
        try:
            query = """
                SELECT i.id, i.name, i.description, i.price, i.type, i.bonus_stat,
                       ui.is_equipped, ui.id as user_item_id
                FROM items i
                JOIN user_items ui ON i.id = ui.item_id
                WHERE ui.user_id = ?
                ORDER BY i.type DESC, ui.acquired_at DESC
            """
            user_items = conn.execute(query, (user_id,)).fetchall()
            return [dict(ui) for ui in user_items]
        except Exception as e:
            print(f"Error getting user items: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_equipped_weapon(user_id):
        """取得玩家當前裝備的武器"""
        conn = get_db_connection()
        try:
            query = """
                SELECT i.*, ui.id as user_item_id
                FROM items i
                JOIN user_items ui ON i.id = ui.item_id
                WHERE ui.user_id = ? AND ui.is_equipped = 1 AND i.type = 'weapon'
                LIMIT 1
            """
            weapon = conn.execute(query, (user_id,)).fetchone()
            return dict(weapon) if weapon else None
        except Exception as e:
            print(f"Error getting equipped weapon: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def buy_item(user_id, item_id):
        """玩家購買商品"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            # 1. 取得商品資訊
            cursor.execute("SELECT price FROM items WHERE id = ?", (item_id,))
            item = cursor.fetchone()
            if not item:
                return False, "商品不存在"
                
            price = item['price']
            
            # 2. 取得玩家金幣
            cursor.execute("SELECT gold FROM characters WHERE user_id = ?", (user_id,))
            char = cursor.fetchone()
            if not char or char['gold'] < price:
                return False, "金幣不足，無法購買"
                
            # 3. 扣除金幣
            cursor.execute("UPDATE characters SET gold = gold - ? WHERE user_id = ?", (price, user_id))
            
            # 4. 塞入玩家背包
            cursor.execute("INSERT INTO user_items (user_id, item_id, is_equipped) VALUES (?, ?, 0)", (user_id, item_id))
            
            conn.commit()
            return True, "購買成功！"
        except Exception as e:
            print(f"Error buying item: {e}")
            conn.rollback()
            return False, "系統錯誤，交易失敗"
        finally:
            conn.close()

    @staticmethod
    def equip_item(user_id, user_item_id):
        """穿戴裝備，並自動卸下同類型的其他裝備"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            # 1. 確保該背包物品存在，且屬於該玩家
            cursor.execute("""
                SELECT ui.id, ui.item_id, i.type 
                FROM user_items ui 
                JOIN items i ON ui.item_id = i.id 
                WHERE ui.id = ? AND ui.user_id = ?
            """, (user_item_id, user_id))
            ui_item = cursor.fetchone()
            if not ui_item:
                return False, "物品不存在於背包中"
                
            item_type = ui_item['type']
            
            # 2. 將同類型的裝備通通解除裝備 (is_equipped = 0)
            cursor.execute("""
                UPDATE user_items 
                SET is_equipped = 0 
                WHERE user_id = ? AND item_id IN (SELECT id FROM items WHERE type = ?)
            """, (user_id, item_type))
            
            # 3. 裝備當前物品
            cursor.execute("UPDATE user_items SET is_equipped = 1 WHERE id = ?", (user_item_id,))
            
            conn.commit()
            return True, "裝備穿戴成功！"
        except Exception as e:
            print(f"Error equipping item: {e}")
            conn.rollback()
            return False, "裝備穿戴失敗"
        finally:
            conn.close()
