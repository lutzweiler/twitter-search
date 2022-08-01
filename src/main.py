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

# search twitter for tweets according to configuration
request = request.TwitterRequest(properties)
request.execute()
result = request.get_result()

# assign a priority value to each tweet and sort them by priority
priority_function = priority.WeightedPriorityFunction
priority = priority.PriorityCalculator(result, priority_function)
priority.calculate_priorities()
priority.sort_by_priority()
tweets = priority.get_tweet_list()

#for tweet in tweets:
#    print(tweet)
#    print("-----------")

# write the result to a csv file
if config.export_csv or config.send_email:
    print("writing results to", config.csv_path)
    with open(config.csv_path, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for tweet in tweets:
            writer.writerow(tweet)

# send the csv file per email
if config.send_email:
    properties = config.get_email_properties()
    print("sending results to", properties.recipient, "via", properties.smtp_server)
    text = "search terms: {}\nnumber of results: {}".format(config.search_terms, len(tweets))
    subject = "Twitter search results"
    mail.send_email(properties, subject, text, config.csv_path)
