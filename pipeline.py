import requests
from authenticate import getToken
import praw
from secret import credentials

user_agent = "canaryScanner by verykarmamuchreddit"

def getData():
    reddit = praw.Reddit(client_id=credentials["clientId"],
    client_secret=credentials["clientSecret"],
    user_agent=user_agent)

    for submission in reddit.subreddit("learnpython").hot(limit=10):
        print(submission.title)

    # headers = {"Authorization": f"bearer {getToken()}", "User-Agent": "canaryScanner by verykarmamuchreddit"}
    # response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    # print(response.json())


if __name__ == "__main__":
    getData()