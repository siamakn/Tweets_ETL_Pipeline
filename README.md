# Tweets_ETL_Pipeline
A docker data pipeline for sentiment analysis of tweets stream


# An ETL process in a Docker data pipeline to analyze the sentiment of tweets stream on a certain topic, using the tweeter API, Vader model and 5 docker containers.


The ETL pipeline is composed of the following containers:

tweet_collector: using the Tweeter API (registration and bearer tocken needed) collects tweets on a certain topic (e.g. #Ukraine)

mongo_for_tweets (MongoDB): is used to store the raw colledted tweets.

etl_job: An ETL job which reads the raw tweets from mongo_for_tweets, cleans the tweets, assigns a polarity score, and inserts the metadata into a PostgreSQL database (db name: mypostgres)

mypostgres: A container to save analyzed tweets metadata

 slack_bot: Finally using a Slackbot template, the highest scored tweet is read from mypostgres and published in a slack channel.