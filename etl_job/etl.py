'''
    Workflow is the following:
    1. Extract the tweets from mongodb
    - connect to a database
    - query the data

    2. TRANSFORM
    - cleaning the text before scoring 
    - score

    3. LOAD
    - connect to a postgres database
    - insert the data to postgres

    Follwong nomenclature was used:
    the name of the mongodb database is "my_mongo_db"
    the name of the collection is "tweets"
    the name of the docker container is "mongo_for_tweets"

    the name of my postgres container is "mypostgres"
    postgres username: "siamak"
    postgres password: "123"
    postgres database name: "postgres_for_tweets"
    postgres table in postgres_for_tweets is called "tweets"
'''

# from pymongo import___

from sqlalchemy import create_engine
import time
import pymongo
import psycopg2
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# To establish a connection to the MongoDB server
client = pymongo.MongoClient(host="mongo_for_tweets", port=27017)

# To select the database to use within the MongoDB server
db = client.my_mongo_db
tweets = db.tweets.find()

# Sleep time was needed! in case the MongoDB is not running in the background:
time.sleep(30)  


# To establish a connection to the Postgres server:

pg = create_engine(
    'postgresql://siamak:123@mypostgres:5432/postgres_for_tweets', echo=True)
# pg = create_engine('postgresql://user:password@host:5432/dbname', echo=True)
# Make sure to insert the same host/username/password/dbname that
# you specified in docker-compose.yml. The host is the name of the container.

# Query to create a table
pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    sentiment NUMERIC
);
''')




# Clean the tweets

mentions_regex = '@[A-Za-z0-9]+'
url_regex = 'https?:\/\/\S+'  # this will not catch all possible URLs
hashtag_regex = '#'
rt_regex = 'RT\s'


def clean_tweets(tweet):
    tweet = re.sub(mentions_regex, '', tweet)  # removes @mentions
    tweet = re.sub(hashtag_regex, '', tweet)  # removes hashtag symbol
    tweet = re.sub(rt_regex, '', tweet)  # removes RT to announce retweet
    tweet = re.sub(url_regex, '', tweet)  # removes most URLs

    return tweet


def sentiment_score(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)['compound']


# Transform the tweets (first clean, then assign polatity score)
texts = [clean_tweets(doc['text']) for doc in tweets]
scores = [sentiment_score(text) for text in texts]

# Load the tweets into the postgres database into the "tweets" table

query = "INSERT INTO tweets VALUES (%s, %s);"

for text, score in zip(texts, scores):
    pg.execute(query, (text, score))
