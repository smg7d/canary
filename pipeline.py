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


if __name__ == "__main__":
    getData()