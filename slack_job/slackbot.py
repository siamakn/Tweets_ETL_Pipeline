import requests
import pandas as pd
import time
import re
from sqlalchemy import create_engine

time.sleep(30)

# Loop for reading tweet from postgresql and post to Slack
while True:
    pg = create_engine('postgresql://postgres:loop@postgresdb:5432/postgres', echo=True)

    query = pg.execute('''SELECT * FROM tweets ORDER BY ID desc limit 1;''')

    kk = str(list(query)[0])
    te = str(re.findall(r'\w.+',kk))
    webhook_url = "https://hooks.slack.com/services/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"
    tweet = {
        "text": te
    }
    requests.post(url=webhook_url, json = tweet)
    time.sleep(30)
