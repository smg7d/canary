import requests
from datetime import timezone, datetime
import time
from authenticate import getToken
import praw
from secret import credentials
from database import Post, PostScores, session

user_agent = "canaryScanner by verykarmamuchreddit"

def addNewPosts(subredditName):
    reddit = praw.Reddit(client_id=credentials["clientId"],
    client_secret=credentials["clientSecret"],
    user_agent=user_agent)

    subreddit = reddit.subreddit(subredditName)

    newPosts = []
    existingPosts = [pId for pId, in session.query(Post.postId)]
    
    for submission in subreddit.new(limit=100):
        if submission.id not in existingPosts:
            post = Post(postId=submission.id, title=submission.title, subreddit=submission.subreddit.display_name, created=int(submission.created_utc), author=submission.author.name)
            newPosts.append(post)

    session.add_all(newPosts)
    session.commit()
    print(f"added {len(newPosts)} new posts")

def addPostScores():
    reddit = praw.Reddit(client_id=credentials["clientId"],
    client_secret=credentials["clientSecret"],
    user_agent=user_agent)

    existingPosts = [p for p in session.query(Post)]

    #get a list of posts
    for existingPost in existingPosts:
        now = int(datetime.now(tz=timezone.utc).timestamp())
        count = len(existingPost.postScores)

        if count > 0:
            postScoreTime = existingPost.postScores[count - 1].age + existingPost.created
            print(f"now is {now} and time is {postScoreTime}, diff is {now - postScoreTime}")
            if (now - postScoreTime > 5*60) and (now - existingPost.created < 60*60*24):
                submission = reddit.submission(id=existingPost.postId)
                age = now - submission.created_utc
                currentPostScore = PostScores(postId=existingPost.postId, score=submission.score, 
                age=age, numberOfComments=submission.num_comments)
                existingPost.postScores.append(currentPostScore)
                session.add(existingPost)
                print(f"post is old, title is {submission.title}")
        else:
            submission = reddit.submission(id=existingPost.postId)
            age = now - submission.created_utc
            currentPostScore = PostScores(postId=existingPost.postId, score=submission.score, 
            age=age, numberOfComments=submission.num_comments)
            existingPost.postScores.append(currentPostScore)
            session.add(existingPost)
            print(f"post is new, title is {submission.title}")

    session.commit()



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
    