import tweepy
import time
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Loading envirenment variables
load_dotenv()

TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
RECEIVER_PHONE_NUMBER = os.getenv('RECEIVER_PHONE_NUMBER')

# Authenticating the TWITTER API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# Scraping the twitter timeline of Elon Musk and getting the latest tweet
tweets = tweepy.Cursor(api.user_timeline,id="elonmusk").items(1)
tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
last_tweet_text = tweets_list[0][2]
last_tweet_id = tweets_list[0][1]

# Authenticating the TWILIO API
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Calling my pesonal number and reading the latest tweet on a phone call
call = client.calls.create(
                        twiml='<Response><Say>Elon Musk just posted a tweet that says: '+ last_tweet_text+ '</Say></Response>',
                        to=RECEIVER_PHONE_NUMBER,
                        from_=TWILIO_PHONE_NUMBER
                    )


'''
# sending the latest tweet as an SMS
message = client.messages \
                .create(
                     body=last_tweet_text,
                     from_=TWILIO_PHONE_NUMBER,
                     to=RECEIVER_PHONE_NUMBER
                 )
'''

# checking for a new tweet every minute
while True:
    tweets = tweepy.Cursor(api.user_timeline,id="elonmusk").items(1)
    tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
    temp_last_tweet_text = tweets_list[0][2]
    temp_last_tweet_id = tweets_list[0][1]

    if last_tweet_id != temp_last_tweet_id:
        last_tweet_id = temp_last_tweet_id
        last_tweet_text = temp_last_tweet_text

        '''
        message = client.messages \
                .create(
                     body=last_tweet_text,
                     from_=TWILIO_PHONE_NUMBER,
                     to=RECEIVER_PHONE_NUMBER
                 )
        '''

        call = client.calls.create(
                        twiml='<Response><Say>Ahoy, World!</Say></Response>',
                        to=RECEIVER_PHONE_NUMBER,
                        from_=TWILIO_PHONE_NUMBER
                    )

    
    time.sleep(60)
