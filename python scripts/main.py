from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
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


class listener(StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data['text']
        print(tweet)
        sentence = TextBlob(tweet)
        print(sentence.sentiment)
        print('-------' * 20)
        time.sleep(0)
        if sentence.subjectivity * 100 >= 60                :
#            output = open('twitter-out.txt', 'a')
#            output.write(str(sentence.polarity))
#            output.write('\n')
#            output.close()
            #print 1
            df = pd.read_csv('twitter-out.csv')
            df = df.append({'polarity': sentence.polarity },ignore_index=True)
#            df.append(sentence.polarity)
            df.to_csv('twitter-out.csv', index = False)

#            with open('twitter-out.csv', 'wb') as csvfile:
#                spamwriter = csv.writer(csvfile, delimiter=',')
#                spamwriter.writerow(sentence.polarity)

        return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=['pakistan'])