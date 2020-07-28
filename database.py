import sqlite3
from sqlite3 import Error


def createConnection(dbFile):
    conn = None
    try:
        conn = sqlite3.connect(dbFile)
        return conn
    except Error as e:
        print(e)
    
    return conn

def createTable(conn, sqlStatement):
    try:
        c = conn.cursor()
        c.execute(sqlStatement)
    except Error as e:
        print(e)

if __name__ == '__main__':
    conn = createConnection(r'/Users/shane/computer/projects/redditBot/canary.db')

    createPostTable = ''' CREATE TABLE IF NOT EXISTS posts (
    postId text PRIMARY KEY,
    title text,
    subreddit text,
    created_utc integer,
    author text
    ); '''

    createVoteTable = ''' CREATE TABLE IF NOT EXISTS votes (
        id integer PRIMARY KEY,
        FOREIGN KEY (postId) REFERENCES posts (postId),
        score integer NOT NULL,
        numberOfComments integer
    ); '''

    createCommentTable = '''

    if conn is not None:
        createTable(conn, createPostTable)
        createTable(conn, createDataTable)