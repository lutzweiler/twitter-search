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

import tweet
import math
import datetime

# this class takes a list of tweets and assigns a priority value
# to each tweet according to a PriorityFunction
# the priority value is a number and a larger number represents greater importance
class PriorityCalculator:
    def __init__(self, tweets, priority_function):
        self.tweets = tweets
        self.priority_function = priority_function

    def calculate_priorities(self):
        for tweet in self.tweets:
            tweet.priority = self.priority_function(tweet)

    def sort_by_priority(self):
        self.tweets = sorted(self.tweets, key = lambda tweet: tweet.priority, reverse = True)

    def get_tweet_list(self):
        return self.tweets

# Example Function, gives every tweet the same priority
def UniformPriorityFunction(tweet):
    return 1

# combines multiple criteria based on a weighted average
def WeightedPriorityFunction(tweet):
    #define weights
    w_time = -0.02 #older tweets are less important than new ones
    #for other attributes we assume more engagement with the tweet makes it more important
    w_followers = 1.0 
    w_verified = 5.0  
    w_likes = 1.0
    w_retweets = 5.0
    w_responses = 2.0
    w_quotes = 2.0

    now = datetime.datetime.now().astimezone()

    #map the criteria to numbers
    #for values that could be in a very wide range, map them to a smaller range using the logarithm
    tweet_age = (now - tweet.time).total_seconds() / 3600 #in hours
    followers = math.log(1 + tweet.user_num_followers)
    verified = 1 if tweet.user_is_verified else 0
    likes = math.log(1 + tweet.num_likes)
    retweets = math.log(1+ tweet.num_retweets)
    responses = math.log(1+ tweet.num_responses)
    quotes = math.log(1+ tweet.num_quotes)

    #compute the weighted average
    priority = 0
    priority += w_time * tweet_age
    priority += w_followers * followers
    priority += w_verified * verified
    priority += w_likes * likes
    priority += w_retweets * retweets
    priority += w_responses * responses
    priority += w_quotes * quotes

    return priority

