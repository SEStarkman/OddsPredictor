import requests
import json


with open("keys.json") as f:
    data = json.load(f)
    host = data["x-rapidapi-host"]
    key = data["x-rapidapi-key"]

# url = "https://api.sportsdata.io/api/nba/fantasy/json/Players"
url = "https://www.espn.com/nba/scoreboard/_/date/20220117"
response = requests.get(url)

if __name__ == "__main__":
    print(response.json())