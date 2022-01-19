import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import datetime
import re
from selenium import webdriver

from requests.api import get


def get_game_ids_by_date_range(sdate, edate):
    game_id_urls = []
    date_list = []
    delta = convert_date(edate) - convert_date(sdate)
    print(delta)

    for i in range(delta.days + 1):
        date = (convert_date(sdate) + datetime.timedelta(days=i)).strftime('%Y%m%d')
        print('date: ', date)
        date_list.append(date)

    for date in date_list:
        url = f'https://www.espn.com/nba/scoreboard/_/date/{date}'
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
        results = soup.find_all('a', href=re.compile(r'/nba/game/_/gameId')) # replace 'game' with 'boxscore' for boxscore, but games not started yet dont show up for boxscore
        # results = soup.select("a[href*=gameId]")
        for i in results:
            print('i: ', i)

        for game in results:
            game_id_urls.append(game['href'])

    print(len(game_id_urls))
    print(game_id_urls)


# def write_game_ids():

def convert_date(date):
    new_date_format = datetime.datetime.strptime(str(date), "%Y-%m-%d").strftime("%Y%m%d")
    new_date_format = datetime.datetime.strptime(new_date_format, '%Y%m%d')

    return new_date_format


def get_first_basket(game_id_url):
    base_url = f'https://www.espn.com{game_id_url}'

    response = requests.get(base_url)
    soup = bs(response.content, 'html.parser')
    q1 = soup.find('div', {'id': "gp-quarter-1"})
    q1_plays = q1.find_all('td', {'class': "game-details"})

    tip_off = q1_plays[0].text
    print('tip off:', tip_off)

    for play in q1_plays:
        if 'makes' in play.text:
            first_score = play.text.split('makes')[0]
            break
        
    print('first score: ', first_score)


if __name__ == '__main__':
    get_game_ids_by_date_range(sdate='2022-01-18', edate='2022-01-18')
    get_first_basket('/nba/playbyplay/_/gameId/401360485')