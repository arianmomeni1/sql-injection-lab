import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS users')

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# کاربر واقعی که هدف حمله است:
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "SuperSecretPassword"))
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("flag_level3_congrajulation", "d"))
conn.commit()
conn.close()
print("Database initialized.")
