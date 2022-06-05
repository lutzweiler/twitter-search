#!/usr/bin/python
import time
import json
import tweepy

token_file = open("bearer_token")
bearer_token = token_file.readline().rstrip()

client = tweepy.Client(bearer_token)
def find_user(includes, user_id):
    for user in includes['users']:
        if user.id == user_id:
            return user
    return None

next_token = None
target_tweets = 5000
tweets_per_page = 100
tweet_count = 0

while tweet_count < target_tweets:
    result = client.search_recent_tweets(
        "phishing lang:de",
        max_results=tweets_per_page,
        expansions="author_id",
        tweet_fields="id,text,author_id,created_at,lang",
        user_fields="id,username,public_metrics,verified",
        next_token=next_token
    )


    data, includes, errors, meta = result
    if data == None:
        break

    if errors == []:
        for tweet in data:
            user = find_user(includes, tweet.author_id)
            print("id:", tweet.id)
            print("time:", tweet.created_at)
            print("user:", user.name, "@"+user.username, "Verified" if user.verified else "")
            print("metrics:", user.public_metrics)
            print("text:")
            print(tweet.text)
            print("")
    else: 
        print("an error has occured")
        print(errors)

    next_token = meta['next_token']
    tweet_count += len(data)
    time.sleep(2)

