import sqlite3
from datetime import datetime

class ItemModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_all(self):
        query = "SELECT * FROM items"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def get_by_id(self, item_id):
        query = "SELECT * FROM items WHERE id = ?"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, (item_id,))
            return cursor.fetchone()

    def add_to_user(self, user_id, item_id):
        query = "INSERT INTO user_items (user_id, item_id) VALUES (?, ?)"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id, item_id))
            conn.commit()

    def get_user_items(self, user_id):
        query = """
        SELECT i.*, ui.is_equipped, ui.id as user_item_id
        FROM items i
        JOIN user_items ui ON i.id = ui.item_id
        WHERE ui.user_id = ?
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            return cursor.fetchall()

    def equip_item(self, user_id, user_item_id, item_type):
        # 先將同類型的裝備解除穿戴
        unequip_query = """
        UPDATE user_items 
        SET is_equipped = 0 
        WHERE user_id = ? AND item_id IN (SELECT id FROM items WHERE type = ?)
        """
        equip_query = "UPDATE user_items SET is_equipped = 1 WHERE id = ?"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(unequip_query, (user_id, item_type))
            cursor.execute(equip_query, (user_item_id,))
            conn.commit()
