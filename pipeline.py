import requests
from datetime import timezone, datetime
import time
from authenticate import getToken
import praw
from secret import credentials
from database import Post, PostScores, Comments, CommentScores, session

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
        if (now - existingPost.created) < 5*60*24*3:

            existingComments = [com.commentId for com in session.query(Comments).filter(Comments.postId==existingPost.postId)]
            #issue delete from comments closures table where postId = postId statement here

            post = reddit.submission(id=existingPost.postId)
            comments = post.comments
            commentList = comments.list()

            levelMap = {}
            for comment in commentList:
                if comment not in existingComments:
                    parentId = comment.parent_id[3:] #trim off prefix of t1_ or t3_
                    levelMap[comment.id] = levelMap.get(parentId, 0) + 1

                    #this is lazy nonetype reference handling. don't judge.
                    author = "" if comment.author is None else comment.author.name 

                    newComment = Comments(commentId=comment.id, parentId=parentId, level=levelMap[comment.id], 
                    author=author, postId=comment.submission, created=int(comment.created_utc), edited=bool(comment.edited))

                    existingPost.comments.append(newComment)
                    commentsAdded += 1
                
                #logic to add to closure table goes here
                '''to add a comment to a closure table, the commentId is the starting point.
                get the parent Id
                while the parentId is not null
                create a new childId parentId combo item
                move the parentId up to the next comment in the tree (call to database)
                '''

                
            session.add(existingPost)
            
    session.commit()
    print(f"{commentsAdded} comments added")

def commentExploring():
    reddit = praw.Reddit(client_id=credentials["clientId"],
    client_secret=credentials["clientSecret"],
    user_agent=user_agent)

    post = reddit.submission(id="hzhttx")
    comments = post.comments
    print(post.title)

    levelMap = {}
    for comment in comments.list():
        parentId = comment.parent_id[3:] #trim off prefix of t1_ or t3_
        levelMap[comment.id] = levelMap.get(parentId, 0) + 1
        
        print(f'''
        some attributes are author: {comment.author}, id: {comment.id},
        parentId: {parentId}, postId: {comment.submission}, level: {levelMap[comment.id]}
        created: {comment.created_utc}, edited: {comment.edited}, and score: {comment.score}''')

def quick():
    # begin = int(datetime.now(tz=timezone.utc).timestamp())
    # time.sleep(5)
    # end = int(datetime.now(tz=timezone.utc).timestamp())
    # print(f'end is {end}, begin is {begin} and diff is {end - begin}')
    reddit = praw.Reddit(client_id=credentials["clientId"],
    client_secret=credentials["clientSecret"],
    user_agent=user_agent)

    submission = reddit.submission(id="i6uv3u")
    print(submission.title)

#need to find out how to get comment Id, parent comment Id

if __name__ == "__main__":
    # quick()
    addNewPosts("ProgrammerHumor")
    addPostScores()
    addNewComments()
    # # commentExploring()


    '''to add a comment to a closure table, the commentId is the starting point.
    get the parent Id
    while the parentId is not null
    create a new childId parentId combo item
    move the parentId up to the next comment in the tree (call to database)

    drop the items in the closure table related to that post at the start and rebuild when it's called


    '''