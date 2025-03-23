import sqlite3
from config import config 

def insertNewTicketForSale(eventAddress: str, ticketId: int, market: str, saler: str, price: float):
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    insert = f"INSERT INTO ticketForsale(eventAddress, ticketId, market, saler, price) VALUES ('{eventAddress}', {ticketId}, '{market}', '{saler}', {price})"
    cursor.execute(insert)
    conn.commit()

    conn.close()
    return True

def getAllTicketOnsale():
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    query = f"SELECT * FROM ticketForsale"
    cursor.execute(query)
    re = cursor.fetchall()

    conn.close()
    return re

def getMarketAddress(eventAddress: str):
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    query = f"SELECT market FROM event WHERE address = '{eventAddress}'"
    cursor.execute(query)
    re = cursor.fetchone()

    conn.close()
    return re[0]

def deleteSoldTicket(eventAddress: str, ticketid: int):
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    insert = f"DELETE FROM ticketForsale  WHERE eventAddress = '{eventAddress}' and ticketId = {ticketid}"
    cursor.execute(insert)
    conn.commit()

    conn.close()
    return True

