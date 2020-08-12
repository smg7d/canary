import sqlite3
from sqlite3 import Error
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# this file creates the tables, declares the objects for the orm
# and provides an interface for the pipeline file to create, read,
# update, and delete

engine = create_engine('sqlite:///canary.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Post(Base):
    __tablename__ = 'posts'
    postId = Column(String, primary_key=True)
    title = Column(String)
    subreddit = Column(String)
    created = Column(Integer)
    author = Column(String)


class PostScores(Base):
    __tablename__ = 'postScores'

    id = Column(Integer, primary_key=True)
    postId = Column(String, ForeignKey('posts.postId'))
    score = Column(Integer)
    age = Column(Integer)
    numberOfComments = Column(Integer)

    post = relationship("Post", back_populates="postScores")

Post.postScores = relationship("PostScores", order_by=PostScores.id, back_populates="post")

Base.metadata.create_all(engine)


# class Comments(Base):
#     __tablename__ = 'comments'

#     commentId = Column(String, primary_key=True)
#     parentId = ForeignKeyField('self', null=True, backref='children')
#     level = IntegerField()
#     author = CharField()
#     postId = ForeignKeyField(Posts, backref='comments')
#     created_utc = BigIntegerField()
#     edited = BooleanField()


# class CommentScores(Base):
#     __tablename__ = 'commentScores'

#     commentId = ForeignKeyField(Comments, backref='commentScores')
#     score = IntegerField()
#     age = IntegerField()

# # Create the tables if they do not exist already


# def createConnection(dbFile):
#     conn = None
#     try:
#         conn = sqlite3.connect(dbFile)
#         return conn
#     except Error as e:
#         print(e)
    
#     return conn

# def createTable(conn, sqlStatement):
#     try:
#         c = conn.cursor()
#         c.execute(sqlStatement)
#     except Error as e:
#         print(e)


# if __name__ == '__main__':
#     Posts.create_table(True)
#     PostScores.create_table(True)
#     Comments.create_table(True)
#     CommentsClosure.create_table(True)
#     CommentScores.create_table(True)
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