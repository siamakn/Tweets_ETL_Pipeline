

import logging
import time

import pymongo
import tweepy
from twitter_keys import *  # import local keys

# To create a connection to the mongodb running in the mongo container of the pipeline
client_docker = pymongo.MongoClient("mongo_for_tweets", port=27017)


# creating a new mongo database in the docker container mongo
db = client_docker.my_mongo_db

# to create a collection:
collection = db.tweets

# AUTHENTICATION and connecting to twitter API
twitter_client = tweepy.Client(bearer_token=BEARER_TOCKEN, wait_on_rate_limit=True)

if twitter_client:
    logging.critical("\nAutentication OK")
else:
    logging.critical('\nVerify your credentials')


# Defining a query search string
search_query = "#Ukraine"
# -is:retweet -is:reply -is:quote -has:links"

# option to extract tweets of a particular language add `lang` parameter eg lang:de

cursor = tweepy.Paginator(
    method=twitter_client.search_recent_tweets,
    query=search_query,
    tweet_fields=['id', 'created_at', 'text'],
    user_fields=['username'],
).flatten(limit=200)

for tweet in cursor:
    record = {'text': tweet.text, 'id': tweet.id,
              'created_at': tweet.created_at}
    db.tweets.insert_one(document=record)
    print(tweet.data)
