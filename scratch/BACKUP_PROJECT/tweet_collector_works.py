# import requests
# from: Intro_Twitter_API_togetherwith_Arjun


# Connect to twitter API
import tweepy
import twitter_keys
client = tweepy.Client(bearer_token=twitter_keys.Bearer_Token)
# - means NOT
search_query = "#Ukraine"
# -is:retweet -is:reply -is:quote -has:links"

# option to extract tweets of a particular language add `lang` parameter eg lang:de

cursor = tweepy.Paginator(
    method=client.search_recent_tweets,
    query=search_query,
    #    tweet_fields=['author_id', 'created_at', 'public_metrics'],
    #    user_fields=['username'],
).flatten(limit=200)

for tweet in cursor:
    print(tweet.data)
