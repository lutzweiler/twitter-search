#!/usr/bin/python
import csv
import jsonpickle
import time
import configuration
import priority
import request
import tweet

config = configuration.Configuration.load_config_file()
properties = config.get_request_properties()

request = request.TwitterRequest(properties)
request.execute()
result = request.get_result()

#Storing the tweets in a file and then loading them again does not make much sense now,
#but will be useful to compare different priority functions on the same data set
#
## serialize
#with open('../data/query_result.json', 'w') as f:
#    s = jsonpickle.encode(result)
#    f.write(s)
# deserialize
#with open('../data/query_result.json', 'r') as f:
#    s = f.read()
#    tweets = jsonpickle.decode(s)

priority_function = priority.WeightedPriorityFunction
priority = priority.PriorityCalculator(result, priority_function)
priority.calculate_priorities()
priority.sort_by_priority()
tweets = priority.get_tweet_list()

for tweet in tweets:
    print(tweet)
    print("-----------")

if config.export_csv:
    with open(config.csv_path, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for tweet in tweets:
            writer.writerow(tweet)
