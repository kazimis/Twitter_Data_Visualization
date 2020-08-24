import tweepy
import csv
import json



# Adding our authentication information
consumer_key = "TlvSP92DtmG0a5hOVFEaC5cIE"
consumer_secret = "QQ0gg1xcSDoMK154OrLAWMUKMe5ApP9SOQrqx4FO0uA5MFKyKD"
access_token = "1262796034217881601-bhLwq0dhjisq3St8eywyVAYhedVuNp"
access_token_secret = "2OwaP5GOwZ6rxknasVS25LoR9mHy0panSVeAhJFzcMwTO"


class myStreamListener(tweepy.StreamListener):
    """" This class is inherited from StreamListener super class"""

    global stream

    def __init__(self, fileName, tweetsNum):
        self.fileName = fileName
        self.tweetsNum = tweetsNum
        self.tweetCount = 0

    def on_data(self, data):
        if self.tweetCount < self.tweetsNum:
            tweet = json.loads(data)
            try:
                text = tweet["extended_tweet"]["full_text"] if "extended_tweet" in data else tweet["text"]
                with open(self.fileName, 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow([tweet["id"], tweet["created_at"],text])
                print(tweet,"\n")
                self.tweetCount += 1
                return True
            except:
                print("error",data)
        else:
            stream.disconnect()

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # number of tweets to be downloaded
    tweetsNum = 1000
    # counter to track number of tweets pulled
    tweetCount = 0
    # Key word that is used to search data from twitter
    tweetWord = "COVID-19"
    # Filename list to store data D1 without query and D2 with query
    withoutQuery = "D1.csv"
    withQuery ="D2.csv"


    # Creating the authentication object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # Setting your access token and secret
    auth.set_access_token(access_token, access_token_secret)
    # Creating the API object while passing in auth information
    api = tweepy.API(auth)

    # pass filename withQuery or withoutQuery
    listener = myStreamListener(withoutQuery,tweetsNum)
    stream = tweepy.Stream(auth, listener,tweet_mode='extended')

    # comment this out to get data with query
    stream.sample(is_async = True,languages=["en"])

    # uncommented to get data with query
    # stream.filter(track = [tweetWord],languages=["en"],encoding='utf8')
