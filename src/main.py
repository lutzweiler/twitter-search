#!/usr/bin/python
import jsonpickle
import time
import priority
import request
import tweet

#token_file = open("bearer_token")
#bearer_token = token_file.readline().rstrip()
#
#properties = request.RequestProperties()
#properties.bearer_token = bearer_token
#properties.search_terms = ["phishing", "phishen", "gefisht"]
#properties.max_results = 500
#
#request = request.TwitterRequest(properties)
#request.execute()
#result = request.get_result()
#
## serialize
#with open('../data/query_result.json', 'w') as f:
#    s = jsonpickle.encode(result)
#    f.write(s)

#Storing the tweets in a file and then loading them again does not make much sense now,
#but will be useful to compare different priority functions on the same data set
 
tweets = []
# deserialize
with open('../data/query_result.json', 'r') as f:
    s = f.read()
    tweets = jsonpickle.decode(s)

priority_function = priority.WeightedPriorityFunction
priority = priority.PriorityCalculator(tweets, priority_function)
priority.calculate_priorities()
priority.sort_by_priority()
tweets = priority.get_tweet_list()

for tweet in tweets:
    print(tweet)
    print("-----------")