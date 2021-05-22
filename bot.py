import tweepy
import re
from datetime import datetime
#import numpy as np
import cv2
import math
import time

consumer_key = ''
consumer_secret = ''

key = ''
secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
#api = tweepy.API(auth, wait_on_rate_limit=True)


FILE_NAME2 = 'last_seen2.txt'

#reads and writes on the last seen tweet file
def read_last_seen2(FILE_NAME2):
    file_read2 = open(FILE_NAME2, 'r')
    last_seen_id2 = int(file_read2.read().strip())
    file_read2.close()
    return last_seen_id2

def store_last_seen2(FILE_NAME2, last_seen_id2):
    file_write2 = open (FILE_NAME2, 'w')
    file_write2.write(str(last_seen_id2))
    return

hashtag = "#feelingold"
tweetNumber = 500



def searchBot():

    latest_tweet = read_last_seen2(FILE_NAME2)
    tweets = tweepy.Cursor(api.search, hashtag, since_id=latest_tweet).items(tweetNumber)

    for tweet in tweets:
        try:
            #api.update_status("@" + tweet.user.screen_name + " Feeling old? Well, I can make you feel worse, use this bot to visualize how long you've been alive in weeks. You just have to @ me with your birthday in the format YYYY-MM-DD. We are not responsible for any life crises or panic attacks that come after.", tweet.id)
            print(tweet.id)
            time.sleep(180)
        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(15)
        #switches out the last seen tweet id
        store_last_seen2(FILE_NAME2, tweet.id)        


FILE_NAME = 'last_seen.txt'

#reads and writes on the last seen tweet file
def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open (FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    return


def reply():
    #makes an array of new tweets
    tweets = api.mentions_timeline(read_last_seen(FILE_NAME), tweet_mode='extended')
    #goes through all the tweets 
    for tweet in reversed(tweets):

        #creates an image with cv2
        img = cv2.imread('img.png', 1)

        #creates a new image
        cv2.imwrite('newimage.jpg', img)

        print (str(tweet.id) + ' - ' + tweet.full_text)
        print (str(tweet.id) + ' - ' + str(tweet.created_at))

        #only runs if there is some resemblance of a date
        if '-' in tweet.full_text.lower():
            #try to run if there is a date in the right format 
            try:

                #gets the date the tweet was created
                created_text = str(tweet.created_at)
                match_created = re.search(r'\d{4}-\d{2}-\d{2}', created_text)
                date_created = datetime.strptime(match_created.group(), '%Y-%m-%d').date()

                #gets the inputted birthday
                birthday_text = str(tweet.full_text)
                match_birthday = re.search(r'\d{4}-\d{2}-\d{2}', birthday_text)
                date_birthday = datetime.strptime(match_birthday.group(), '%Y-%m-%d').date()

                #gets the age, weeks alive and years alive (all rounded)
                age = date_created - date_birthday
                print ("age: " + str(age))
                weeks_alive = (age.days)/7
                print ("weeks alive: " + str(weeks_alive))
                years = math.floor(age.days/365)
                print ("years: " + str(years))
                color_b = 218
                color_g = 181
                color_r = 200

                if years > 0  and years < 90:
                    #adds a square for all the complete squares
                    for x in range (years):
                        for y in range (52):
                            if x <= 4:
                                color_b = 255
                                color_g = 158
                                color_r = 48
                            elif x<=13:
                                color_b = 193
                                color_g = 189
                                color_r = 54
                            elif x<=17:
                                color_b = 69
                                color_g = 255
                                color_r = 66
                            elif x<=21:
                                color_b = 37
                                color_g = 145
                                color_r = 252
                            elif x<=62:
                                color_b = 53
                                color_g = 43
                                color_r = 255
                            else: 
                                color_b = 218
                                color_g = 181
                                color_r = 200
                                
                            img = cv2.rectangle(img, (117+(y*20),228+(x*18)), (129+(y*20),240+(x*18)), (color_b, color_g, color_r), -1)

                    new_year_days = age.days - years*365
                    new_year_weeks = round(new_year_days/7)

                    #adds a square for the squares in the current year
                    for z in range (new_year_weeks):
                        img = cv2.rectangle(img, (117+(z*20), 228+(years*18)), (129+(z*20),240+(years*18)), (color_b,color_g,color_r), -1)
                    
                    print ('New year days: ' + str (new_year_days))
                    print ('New year weeks: ' + str(new_year_weeks))

                    #updates the new image file
                    cv2.imwrite('newimage.jpg', img)
                    media = api.media_upload("newimage.jpg")


                    #sends the tweet
                    #api.update_status("@" + tweet.user.screen_name + 
                    #" Heyooo!! You've been alive for " + str(round(weeks_alive)) + "week. Here's a graphical representation of your life in weeks you've lived and how many you've got left until 90. #lifeinweeks", 
                   # tweet.id, media_ids=[media.media_id])
                    #api.create_favorite(tweet.id)
                    
            except AttributeError:
                print("Wrong date")

        #switches out the last seen tweet id
        store_last_seen(FILE_NAME, tweet.id)

while True:
    reply()
   #searchBot()
    time.sleep(2)

