import requests
from bs4 import BeautifulSoup as bs
import json

def get_first_basket(game_id):
    base_url = f'https://www.espn.com/nba/boxscore/_/gameId/{game_id}'

    