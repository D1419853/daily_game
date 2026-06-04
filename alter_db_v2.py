import sqlite3
import os
from datetime import date

db_path = os.path.join('instance', 'database.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

columns_to_add = [
    ("current_hp", "INTEGER DEFAULT 100"),
    ("max_hp", "INTEGER DEFAULT 100"),
    ("daily_goal", "INTEGER DEFAULT 3"),
    ("tasks_done_today", "INTEGER DEFAULT 0"),
    ("last_active_date", "DATE")
]

for col_name, col_type in columns_to_add:
    try:
        c.execute(f'ALTER TABLE characters ADD COLUMN {col_name} {col_type}')
        print(f"Added {col_name} column")
    except sqlite3.OperationalError as e:
        print(f"Column {col_name} might already exist or error: {e}")

# Set initial last_active_date for existing characters so they don't instantly take damage on first login
today_str = date.today().isoformat()
c.execute("UPDATE characters SET last_active_date = ? WHERE last_active_date IS NULL", (today_str,))

conn.commit()
conn.close()
print("Database schema update complete.")
