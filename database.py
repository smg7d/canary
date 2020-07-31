import sqlite3
from sqlite3 import Error
from peewee import * 
from playhouse.sqlite_ext import *

db = SqliteDatabase('canary.db')
db.load_extension('./closure')

class Posts(Model):
    postId = CharField(primary_key=True)
    title = CharField()
    subreddit = CharField()
    created_utc = BigIntegerField()
    author = CharField()

    class Meta:
        database = db


class PostScores(Model):
    postId = ForeignKeyField(Posts, backref='postScores')
    score = IntegerField()
    age = IntegerField()
    numberOfComments = IntegerField()

    class Meta:
        database = db

class Comments(Model):
    commentId = CharField(primary_key=True)
    parentId = ForeignKeyField('self', null=True, backref='children')
    level = IntegerField()
    author = CharField()
    postId = ForeignKeyField(Posts, backref='comments')
    created_utc = BigIntegerField()
    edited = BooleanField()

    class Meta:
        database = db

CommentsClosure = ClosureTable(Comments)

class CommentScores(Model):
    commentId = ForeignKeyField(Comments, backref='commentScores')
    score = IntegerField()
    age = IntegerField()

# Create the tables if they do not exist already


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
    Posts.create_table(True)
    PostScores.create_table(True)
    Comments.create_table(True)
    CommentsClosure.create_table(True)
    CommentScores.create_table(True)
    # conn = createConnection(r'/Users/shane/computer/projects/redditBot/canary.db')

    # createPostTable = ''' CREATE TABLE IF NOT EXISTS posts (
    # postId text PRIMARY KEY,
    # title text,
    # subreddit text,
    # created_utc integer,
    # author text
    # ); '''

    # createVoteTable = ''' CREATE TABLE IF NOT EXISTS votes (
    #     id integer PRIMARY KEY,
    #     FOREIGN KEY (postId) REFERENCES posts (postId),
    #     score integer NOT NULL,
    #     numberOfComments integer
    # ); '''

    # createCommentTable = '''

    # if conn is not None:
    #     createTable(conn, createPostTable)
    #     createTable(conn, createDataTable)