"""
manutd.py
A script that tweets Manchester United Premier League statistics every 12 hours
The twitter account used is @21iscoming_
Author: Ankur Dahal
Date:   12/31/2020
"""
import os
import time
from os import environ

import tweepy
from soccer_data_api import SoccerDataAPI

# return a text progress bar showing the proportion of matches played 
def createProgressBar(matches):
    total_len = 38
    return "[" + (matches - 1) * ":" + ">" + (total_len - matches) * "." + "]" 

# write num to filename
def updateNumber(num, filename):
    file = open(filename, 'w')
    file.write(str(num))
    file.close()
    return

# read the number from the file
def getUpdateNumber(filename):
    file = open(filename, 'r')
    num = int(file.read())
    file.close()
    return num

def setUpOAuth():
    auth = tweepy.OAuthHandler(environ['consumer_key'], environ['consumer_secret'])
    auth.set_access_token(environ['access_token'], environ['access_token_secret'])
    return auth

def constructTweet(team, points_diff, update_num):
    progress_bar = createProgressBar(int(team['matches_played']))
    record = f"{team['wins']}-{team['draws']}-{team['losses']}"
    tweet =  f"Manchester United PL Update #{update_num}\n"
    tweet += f"Current Position : {team['pos']}\nPoints : {team['points']}\n"
    tweet += f"Points off top : {points_diff}\nRecord (W-D-L) : {record}\n"
    tweet += f"Season Progress : {progress_bar} ({team['season_progress']}%)\n"
    tweet += "#21ISCOMING #GGMU\n"
    return tweet


def main():
    twitter_api = tweepy.API(setUpOAuth(), wait_on_rate_limit = True)
    soccer_data = SoccerDataAPI()
    epl = soccer_data.english_premier()
    man_utd = [club for club in epl if club['team'] == "Manchester Utd"][0]
    
    # calculate the % of matches played 
    man_utd['season_progress'] = round((int(man_utd['matches_played']) / 38) * 100, 1)

    # file to store the update counter
    filename = "update_counter.txt"

    update_num = getUpdateNumber(filename)
    points_diff = int(epl[0]['points']) - int(man_utd['points'])
    tweet = constructTweet(man_utd, points_diff, update_num)
    updateNumber(update_num + 1, filename)

    try:
        twitter_api.update_status(tweet)
        print(tweet)
    except tweepy.TweepError as e:
        print(e.reason)


if __name__ == "__main__":
    main()