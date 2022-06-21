import tweet

class PriorityCalculator:
    def __init__(self, tweets, priority_function):
        self.tweets = tweets
        self.priority_function = priority_function

    def calculate_priorities(self):
        for tweet in self.tweets:
            tweet.priority = self.priority_function(tweet)

#Example Function, gives every tweet the same priority
def UniformPriorityFunction(tweet):
    return 1
