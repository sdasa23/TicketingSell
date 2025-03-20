import sqlite3
from config import config 

def isNewUser(address: str):
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    query = f"SELECT * FROM user WHERE address = '{address}'" 
    cursor.execute(query)
    re = cursor.fetchall()
    conn.close()
    if(len(re) == 0):
        return False
    else:
        return True
    
def insertNewUser(address: str):
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    insert = f"INSERT INTO user VALUES ('{address}')"
    cursor.execute(insert)
    conn.commit()

    conn.close()
    return True