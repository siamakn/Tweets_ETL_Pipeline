FROM python:3.8-slim-buster

WORKDIR /app

# COPY requirements.txt requirements.txt

COPY . /app 

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD [ "python3", "tweet_collector.py"]
