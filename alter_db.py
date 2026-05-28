import sqlite3
import os

db_path = os.path.join('instance', 'database.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

try:
    c.execute('ALTER TABLE tasks ADD COLUMN duration_minutes INTEGER DEFAULT 0')
    print("Added duration_minutes column")
except sqlite3.OperationalError as e:
    print(f"Error adding duration_minutes: {e}")

try:
    c.execute('ALTER TABLE tasks ADD COLUMN unlock_at DATETIME')
    print("Added unlock_at column")
except sqlite3.OperationalError as e:
    print(f"Error adding unlock_at: {e}")

conn.commit()
conn.close()
