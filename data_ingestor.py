import requests
import json


with open("keys.json") as f:
    data = json.load(f)
    host = data["x-rapidapi-host"]
    key = data["x-rapidapi-key"]

# response = requests.get("https://api-nba-v1.p.rapidapi.com/teams/teamId/", headers=data)
response = requests.get("https://api.sportsdata.io/api/nba/fantasy/json/Players")

if __name__ == "__main__":
    print(response.json())