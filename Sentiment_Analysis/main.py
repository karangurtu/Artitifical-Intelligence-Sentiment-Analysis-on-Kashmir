from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import time
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import csv
import pandas as pd


ckey = 'dl2C9UePjgyidl6SkQPTEtzaK'
csecret = 'KS9B1FZnfDVvyz8hbDMGV0rMYqDDcLue78atS8iG0CO4iUEfkR'
atoken = '827462914579787777-OM3bcV4tu7WuKrKjnIVUNhQ4NEOOJ5T'
asecret = 'upBgJ3LPF4siuwrsTpxYoEsgOPT2QPaA6jw4jsoTkTaOF'

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

i = input("""Press 1 for Streaming\nPress 2 for Normal\n""")

if i==1:
    class listener(StreamListener):
        def on_data(self, data):
            all_data = json.loads(data)
            tweet = all_data['text']
            print tweet
            sentence = TextBlob(tweet)
            print sentence.sentiment
            print '-------' * 20
            time.sleep(0)
            if sentence.subjectivity * 100 >= 60:
                df = pd.read_csv('twitter-out.csv')
                df = df.append({'polarity': sentence.polarity },ignore_index=True)
                df.to_csv('twitter-out.csv', index = False)

            return True

        def on_error(self, status):
            print status


    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=['pakistan'])

elif i==2:
    api = tweepy.API(auth)
    public_tweets = api.search(q="pakistan supreme court", count=20)
    for tweet in public_tweets:
        print tweet
        sentence = TextBlob(tweet.text)
        print sentence.sentiment
        print '-------' * 20
        time.sleep(0)
        if sentence.subjectivity * 100 >= 60:
            df = pd.read_csv('twitter-normal-out.csv')
            df = df.append({'polarity': sentence.polarity}, ignore_index=True)
            df.to_csv('twitter-normal-out.csv', index=False)
