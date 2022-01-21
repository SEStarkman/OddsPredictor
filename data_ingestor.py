import requests
import json


with open("keys.json") as f:
    data = json.load(f)
    key = data["key"]

url = "https://api.sportsdata.io/api/nba/fantasy/json/Players"
response = requests.get(url)

if __name__ == "__main__":
    print(response.json())