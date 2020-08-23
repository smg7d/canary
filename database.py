import sqlite3
from sqlite3 import Error
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


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


class Comments(Base):
    __tablename__ = 'comments'

    commentId = Column(String, primary_key=True)
    parentId = Column(String)
    level = Column(Integer)
    author = Column(String)
    postId = Column(String, ForeignKey('posts.postId'))
    created = Column(Integer)
    edited = Column(Boolean)
    commentText = Column(String)

    post = relationship("Post", back_populates="comments")
    closures = relationship("CommentsClosure", back_populates="comments")


class CommentsClosure(Base):
    __tablename__ = 'commentsClosure'
    id = Column(Integer, primary_key=True)
    parentId = Column(String)
    childId = Column(String)
    postId = Column(String, ForeignKey('comments.postId'))


class CommentScores(Base):
    __tablename__ = 'commentScores'

    id = Column(Integer, primary_key=True)
    commentId = Column(String, ForeignKey('comments.commentId'))
    score = Column(Integer)
    age = Column(Integer)

    comment = relationship("Comments", back_populates="commentScores")

Post.postScores = relationship("PostScores", order_by=PostScores.id, back_populates="post")
Post.comments = relationship("Comments", order_by=Comments.created, back_populates="post" )
Comments.commentScores = relationship("CommentScores", order_by=CommentScores.id, back_populates="comment")
Comments.commentsClosures = relationship("CommentsClosure", order_by=CommentsClosure.id, back_populates="comments")
CommentsClosure.comments = relationship("Comments", order_by=Comments.commentId, back_populates="commentsClosures")

Base.metadata.create_all(engine)