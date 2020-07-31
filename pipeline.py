import requests
from authenticate import getToken
import praw
from secret import credentials

user_agent = "canaryScanner by verykarmamuchreddit"

def getData():
    reddit = praw.Reddit(client_id=credentials["clientId"],
    client_secret=credentials["clientSecret"],
    user_agent=user_agent)

    subreddit = reddit.subreddit("ProgrammerHumor")
    

    for submission in subreddit.hot(limit=10):
        print(f'''
        id is {submission.id}, title is {submission.title}, author is {submission.author}, time created is {submission.created_utc}, score is {submission.score}, and number of comments is {submission.num_comments} and name is {submission.name}, and permalink is {submission.permalink}
        ''')

        lastSubmission = submission

    print(f'now this is the last submission: {lastSubmission.title}')


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


#need to find out how to get comment Id, parent comment Id

if __name__ == "__main__":
    commentExploring()