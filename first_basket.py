from numpy import NaN
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
import re


def get_game_ids_by_date_range(sdate, edate):
    game_id_urls = []
    gameid_date = []
    date_list = []
    delta = convert_date(edate) - convert_date(sdate)

    for i in range(delta.days + 1):
        date = (convert_date(sdate) + datetime.timedelta(days=i)).strftime('%Y%m%d')
        date_list.append(date)

    for date in date_list:
        url = f'https://www.espn.com/nba/scoreboard/_/date/{date}'
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
        results = soup.find_all('a', href=re.compile(r'/nba/game/_/gameId')) # replace 'game' with 'boxscore' for boxscore, but games not started yet dont show up for boxscore

        for game in results:
            game_id_urls.append(game['href'].replace('game', 'playbyplay', 1))
            gameid_date.append(date)

    return game_id_urls, gameid_date

def convert_date(date):
    new_date_format = datetime.datetime.strptime(str(date), "%Y-%m-%d").strftime("%Y%m%d")
    new_date_format = datetime.datetime.strptime(new_date_format, '%Y%m%d')

    return new_date_format


def get_first_basket(game_id_url):
    try:
        base_url = f'https://www.espn.com{game_id_url}'

        response = requests.get(base_url)
        soup = bs(response.content, 'html.parser')
        q1 = soup.find('div', {'id': "gp-quarter-1"})
        q1_plays = q1.find_all('td', {'class': "game-details"})

        for play in q1_plays:
            if 'vs.' in play.text and play.text != 'vs.':
                tip_off = play.text
                break
            else:
                tip_off = NaN

        for play in q1_plays:
            if 'makes' in play.text:
                first_score = play.text.split('makes')[0]
                break
            else:
                first_score = NaN
        
        return tip_off, first_score
    except AttributeError:
        return NaN, NaN

def create_table(game_id_urls):
    indices = []
    features = ['date', 'tip_off', 'first_scorer']
    for index in game_id_urls:
        indices.append(index.split('gameId/')[1])
    df = pd.DataFrame(index=indices, columns=features)

    return df


if __name__ == '__main__':
    sdate = '2021-10-19' # Start of 2021-2022 season
    # edate = '2021-11-10'
    # sdate = '2022-01-16'
    edate = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    game_id_urls, gameid_date = get_game_ids_by_date_range(sdate, edate)
    df = create_table(game_id_urls)
    df['date'] = gameid_date
    for url in game_id_urls:
        gameid = url.split('gameId/')[1]
        tip_off, first_score = get_first_basket(url)
        df['tip_off'][gameid] = tip_off
        df['first_scorer'][gameid] = first_score
    
    print(df)
    df.to_csv('first_score.csv')
