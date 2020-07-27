import sqlite3
from sqlite3 import Error


def createConnection(dbFile):
    conn = None
    try:
        conn = sqlite3.connect(dbFile)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    createConnection(r'/Users/shane/computer/projects/redditBot/canary.db')