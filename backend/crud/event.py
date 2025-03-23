import sqlite3
from config import config 

def insertNewEvent(name: str, symbol: str, address: str, market: str, organizer: str):
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    insert = f"INSERT INTO event(name, symbol, address, market, organizer) VALUES ('{name}', '{symbol}', '{address}', '{market}', '{organizer}')"
    cursor.execute(insert)
    conn.commit()

    conn.close()
    return True

def getAllEvents():
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    query = "SELECT * FROM event"
    cursor.execute(query)
    re = cursor.fetchall()

    conn.close()
    return re
