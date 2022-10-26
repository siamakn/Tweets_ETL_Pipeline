import requests
import pandas as pd
import time
import re
from sqlalchemy import create_engine

time.sleep(30)

# Loop for reading tweet from postgresql and post to Slack
while True:
    pg = create_engine(
        'postgresql://siamak:123@mypostgres:5432/postgres_for_tweets', echo=True)

    query = pg.execute('''SELECT * FROM tweets ORDER BY ID desc limit 1;''')

    kk = str(list(query)[0])
    te = str(re.findall(r'\w.+',kk))
    webhook_url = "https://hooks.slack.com/services/tofill"
    tweet = {
        "text": te
    }
    requests.post(url=webhook_url, json = tweet)
    time.sleep(600)
