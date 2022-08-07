#!/usr/bin/python
import csv
import jsonpickle
import time
import configuration
import mail
import priority
import request
import tweet

# load the configuration from a file
config = configuration.Configuration.load_config_file()
properties = config.get_request_properties()

old_tweets = []
most_recent_time = None
try:
    with open(config.csv_path, 'r') as f:
        reader = csv.reader(f, delimiter=';', quotechar='"')
        next(reader) # skip header
        for row in reader:
            t= tweet.Tweet()
            t.from_argument_list(*row)
            t.priority = None
            t.time = datetime.datetime.strptime(t.time, "%Y-%m-%d %H:%M:%S")
            old_tweets.append(t)
    old_tweets = sorted(tweets, key = lambda t: t.time, reverse = True)
    most_recent_time = old_tweets[0].time
except:
    pass
print(most_recent_time)

# search twitter for tweets according to configuration
properties.time_cutoff = most_recent_time
request = request.TwitterRequest(properties)
request.execute()
result = request.get_result()
result = result + old_tweets

# assign a priority value to each tweet and sort them by priority
priority_function = priority.WeightedPriorityFunction
priority = priority.PriorityCalculator(result, priority_function)
priority.calculate_priorities()
priority.sort_by_priority()
tweets = priority.get_tweet_list()


# write the result to a csv file
if config.export_csv or config.send_email:
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

# send the csv file per email
if config.send_email:
    properties = config.get_email_properties()
    print("sending results to", properties.recipient, "via", properties.smtp_server)
    text = "search terms: {}\nnumber of results: {}".format(config.search_terms, len(tweets))
    subject = "Twitter search results"
    mail.send_email(properties, subject, text, config.csv_path)
