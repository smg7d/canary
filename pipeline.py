import requests
from authenticate import getToken


def getData():
    headers = {"Authorization": f"bearer {getToken()}", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    print(response.json())


if __name__ == "__main__":
    getData()