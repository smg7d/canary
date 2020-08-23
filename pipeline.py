import requests
from datetime import timezone, datetime
import time
from authenticate import getToken
import praw
from secret import credentials
from database import Post, PostScores, Comments, CommentsClosure, CommentScores, session

user_agent = "canaryScanner by verykarmamuchreddit"

reddit = praw.Reddit(client_id=credentials["clientId"],
    client_secret=credentials["clientSecret"],
    user_agent=user_agent)

def addNewPosts(subredditName):

    subreddit = reddit.subreddit(subredditName)

    newPosts = []
    existingPosts = [pId for pId, in session.query(Post.postId)]
    
    for submission in subreddit.new(limit=100):
        if submission.id not in existingPosts:
            post = Post(postId=submission.id, title=submission.title, subreddit=submission.subreddit.display_name, 
            created=int(submission.created_utc), author=submission.author.name)
            newPosts.append(post)

    session.add_all(newPosts)
    session.commit()
    print(f"added {len(newPosts)} new posts")

def addPostScores():

    existingPosts = [p for p in session.query(Post)]

    #get a list of posts
    for existingPost in existingPosts:
        now = int(datetime.now(tz=timezone.utc).timestamp())
        count = len(existingPost.postScores)

        if count > 0:
            postScoreTime = existingPost.postScores[count - 1].age + existingPost.created
            if (now - postScoreTime > 5*60) and (now - existingPost.created < 60*60*24):
                post = reddit.submission(id=existingPost.postId)
                age = now - post.created_utc
                currentPostScore = PostScores(postId=existingPost.postId, score=post.score, 
                age=age, numberOfComments=post.num_comments)
                existingPost.postScores.append(currentPostScore)
                session.add(existingPost)
                print(f"updating score for {post.title}")
        else:
            post = reddit.submission(id=existingPost.postId)
            age = now - post.created_utc
            currentPostScore = PostScores(postId=existingPost.postId, score=post.score, 
            age=age, numberOfComments=post.num_comments)
            existingPost.postScores.append(currentPostScore)
            session.add(existingPost)
            print(f"initial score for {post.title}")

    session.commit()

def addNewComments():
    now = int(datetime.now(tz=timezone.utc).timestamp())
    commentsAdded = 0

    existingPosts = [p for p in session.query(Post)]
    for existingPost in existingPosts:
        if (now - existingPost.created) < 60*60*24:

            existingComments = [com.commentId for com in session.query(Comments).filter(Comments.postId==existingPost.postId)]
            #issue delete from comments closures table where postId = postId statement here

            post = reddit.submission(id=existingPost.postId)
            post.comments.replace_more(limit=None)
            commentList = post.comments.list()

            levelMap = {}
            for comment in commentList:
                if comment not in existingComments:
                    parentId = comment.parent_id[3:] #trim off prefix of t1_ or t3_
                    levelMap[comment.id] = levelMap.get(parentId, 0) + 1

                    #this is lazy nonetype reference handling. don't judge.
                    try:
                        author = "" if comment.author is None else comment.author.name 
                    except:
                        author = ""

                    newComment = Comments(commentId=comment.id, parentId=parentId, level=levelMap[comment.id], commentText=comment.body,
                    author=author, postId=comment.submission, created=int(comment.created_utc), edited=bool(comment.edited))

                    existingPost.comments.append(newComment)
                    commentsAdded += 1
                
                #logic to add to closure table goes here
                parentId = comment.parent_id[3:] #starts at the existing parent
                existingComment = session.query(Comments).filter(Comments.commentId == comment.id).one()
                while(parentId != existingComment.postId):
                    newCommentClosure = CommentsClosure(parentId=parentId, childId=existingComment.commentId, postId=existingComment.postId)
                    existingComment.commentsClosures.append(newCommentClosure)

                    parentComment = session.query(Comments).filter(Comments.commentId == parentId).one()
                    if parentComment is None:
                        break

                    parentId = parentComment.parentId

                session.add(existingComment)
               
            session.add(existingPost)
            
    session.commit()
    print(f"{commentsAdded} comments added")

def addCommentScores():
    existingComments = session.query(Comments).all()

    #get a list of posts
    for existingComment in existingComments:
        now = int(datetime.now(tz=timezone.utc).timestamp())
        count = len(existingComment.commentScores)

        if count > 0:
            commentScoreTime = existingComment.commentScores[count - 1].age + existingComment.created
            if (now - commentScoreTime > 5*60) and (now - existingComment.created < 60*60*24):
                feedComment = reddit.comment(id=existingComment.commentId)
                age = now - existingComment.created
                newCommentScore = CommentScores(commentId=existingComment.commentId, score=feedComment.score, 
                age=age)
                existingComment.commentScores.append(newCommentScore)
                session.add(existingComment)
                print(f"updating score for {existingComment.commentId}")
        else:
            feedComment = reddit.comment(id=existingComment.commentId)
            age = now - existingComment.created
            newCommentScore = CommentScores(commentId=existingComment.commentId, score=feedComment.score, 
            age=age)
            existingComment.commentScores.append(newCommentScore)
            session.add(existingComment)
            print(f"initial score for {existingComment.commentId}")

    session.commit()


def quick():
    # begin = int(datetime.now(tz=timezone.utc).timestamp())
    # time.sleep(5)
    # end = int(datetime.now(tz=timezone.utc).timestamp())
    # print(f'end is {end}, begin is {begin} and diff is {end - begin}')
    reddit = praw.Reddit(client_id=credentials["clientId"],
    client_secret=credentials["clientSecret"],
    user_agent=user_agent)

    submission = reddit.comment(id="g1dpr0t")
    print(submission.score)

#need to find out how to get comment Id, parent comment Id

def monitoring():
    #os.path.getsize("canary.db")

    #texts number of posts and comments added, as well as file size of database

    #on error text error hit
    pass

if __name__ == "__main__":
    # quick()
    addNewPosts("ProgrammerHumor")
    addPostScores()
    addNewComments()
    addCommentScores()
    # commentExploring()
