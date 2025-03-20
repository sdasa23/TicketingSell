
import sqlite3

# If the TrustTix isn`t existed, create a databse called TrustTix
db_path = "../TrustTix.db"
conn = sqlite3.connect(db_path)

cursor = conn.cursor()

# create user table to check the user is whether a fresh man.
cursor.execute("""
CREATE TABLE IF NOT EXISTS user(
    address TEXT PRIMARY KEY                
);
""")

conn.commit()


cursor.execute("""
CREATE TABLE IF NOT EXISTS event(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    symbol TEXT NOT NULL,
    address TEXT NOT NULL,
    market TEXT NOT NULL,
    organizer TEXT NOT NULL
);
""")

conn.commit()

conn.close()

