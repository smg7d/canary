import requests
import requests.auth
from secret import credentials

client_auth = requests.auth.HTTPBasicAuth(credentials["clientId"], credentials["clientSecret"])
post_data = {"grant_type" : "password", "username": credentials["userName"], "password": credentials["password"]}
headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}


def getToken():
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    json = response.json()
    return json["access_token"]

if __name__ == "__main__":
    print(getToken())