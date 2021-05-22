import tweepy
import re
from datetime import datetime
#import numpy as np
import cv2
import math
import time

consumer_key = '8oVbGaOL2QWokdEYnKCIfukvB'
consumer_secret = 'tzA7oyyMfAOl9QdSDKTq76WFEEkB4OBBN6vAZm4UeK4i1Xg4Zt'

key = '1341144942899544067-DSWbYVBz14ccOe2JPeA95LEsq9sBV4'
secret = 'gEVeA7Ujgw7n8zO7ZEjKm9yLSEdWIJT1zMvt2I92yFWia'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)
#api = tweepy.API(auth, wait_on_rate_limit=True)


hashtag = "#feelingold"
tweetNumber = 100

tweets = tweepy.Cursor(api.search, hashtag).items(tweetNumber)

def searchBot():
    for tweet in tweets:
        try:
            api.update_status("@" + tweet.user.screen_name + " Feeling old? Well, I can make you feel worse, use this bot to visualize how long you've been alive in weeks. You just have to @ me with your birthday in the format YYYY-MM-DD. We are not responsible for any life crises or panic attacks that come after. #lifeinweeks", tweet.id)
            api.create_favorite(tweet.id)
            print(tweet.id)
            time.sleep(15)
        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(15)

searchBot()
