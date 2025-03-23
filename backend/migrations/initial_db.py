
import sqlite3
import os

# If the TrustTix isn`t existed, create a databse called TrustTix
db_path = "../TrustTix.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print("DELETE EXISTED DATABASE")
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS ticketForsale(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eventAddress TEXT NOT NULL,
    ticketId INTEGER NOT NULL,
    market TEXT NOT NULL,
    saler TEXT NOT NULL,
    price REAL NOT NULL
);
""")

conn.commit()

conn.close()

