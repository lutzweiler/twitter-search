#!/usr/bin/python
"""
MIT License

Copyright (c) 2022 Lutzweiler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import csv
import time
import datetime
from flask import Flask
from flask import jsonify
import configuration
import mail
import priority
import request
import tweet


RUN_MODE = 0

RUN_COMMAND_LINE = 1
RUN_FLASK = 2

if __name__ == "__main__":
    print("running in command line mode")
    RUN_MODE = RUN_COMMAND_LINE
else:
    print("running in flask mode")
    RUN_MODE = RUN_FLASK

def write_tweets_to_file():
    print("writing results to", config.csv_path)
    with open(config.csv_path, 'w') as f:
        writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(["id",
            "time",
            "text",
            "user_at_name",
            "user_display_name",
            "user_num_followers",
            "user_is_verified",
            "num_likes",
            "num_retweets",
            "num_responses",
            "num_quotes",
            "priority",
            "done"]
        )
        for tweet in tweets:
            writer.writerow(tweet)

# load the configuration from a file
config = configuration.Configuration.load_config_file()
properties = config.get_request_properties()

tweets = []
most_recent_time = None
try:
    with open(config.csv_path, 'r') as f:
        reader = csv.reader(f, delimiter=';', quotechar='"')
        next(reader) # skip header
        for row in reader:
            t= tweet.Tweet()
            t.from_argument_list(*row)
            t.num_likes = int(t.num_likes) #apparently, csv reader interprets everything as a str
            t.num_retweets = int(t.num_retweets)
            t.num_responses = int(t.num_responses)
            t.num_quotes = int(t.num_quotes)
            t.user_num_followers = int(t.user_num_followers)
            t.id = int(t.id)
            t.user_is_verified = True if t.user_is_verified == "True" else False
            t.done = True if t.done == "True" else False
            t.time = datetime.datetime.strptime(t.time[:-3] + t.time[-2:], "%Y-%m-%d %H:%M:%S%z") #remove the colon in the timezone offset for compatibility with the parsing library
            tweets.append(t)
    tweets = sorted(tweets, key = lambda t: t.time, reverse = True)
    most_recent_time = tweets[0].time
except:
    pass

# update the tweet list
properties.time_cutoff = most_recent_time
request = request.TwitterRequest(properties)
request.execute()
result = request.get_result()
tweets = result + tweets

# assign a priority value to each tweet and sort them by priority
priority_function = priority.WeightedPriorityFunction
priority = priority.PriorityCalculator(tweets, priority_function)
priority.calculate_priorities()
priority.sort_by_priority()
tweets = priority.get_tweet_list()

print(len(tweets))
# if run throught flask start the flask app
if RUN_MODE == RUN_FLASK:
    app = Flask(__name__)

    @app.route("/tweets/")
    def get_tweet_list():
        tweet_ids = []
        for t in tweets:
            tweet_ids.append(str(t.id)) #use strings for ids because as integers they are larger than the max size
        return jsonify(tweet_ids)

    @app.route("/tweets/<tweet_id>")
    def get_tweet(tweet_id):
        for t in tweets:
            if t.id == int(tweet_id):
                return jsonify(vars(t))
        return ('', 404) 

    @app.route("/tweets/<tweet_id>/done", methods=['GET','POST'])
    def mark_tweet_done(tweet_id):
        for t in tweets:
            if t.id == int(tweet_id):
                print("x")
                t.done = True
                write_tweets_to_file()
        return ('', 200)

    @app.route("/tweets/<tweet_id>/undone", methods=['GET','POST'])
    def mark_tweet_undone(tweet_id):
        for t in tweets:
            if t.id == int(tweet_id):
                print("x")
                t.done = False
                write_tweets_to_file()
        return ('', 200)


if RUN_MODE == RUN_COMMAND_LINE:
    write_tweets_to_file()

    # send the csv file per email
    if config.send_email:
        properties = config.get_email_properties()
        print("sending results to", properties.recipient, "via", properties.smtp_server)
        text = "search terms: {}\nnumber of results: {}".format(config.search_terms, len(tweets))
        subject = "Twitter search results"
        mail.send_email(properties, subject, text, config.csv_path)
