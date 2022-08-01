# this class contains data, metadata and metrics for a single tweet
class Tweet:
    def __init__(self):
        self.id = None
        self.time = None
        self.text = None
        self.user_at_name = None
        self.user_display_name = None
        self.user_num_followers = None
        self.user_is_verified = None
        self.num_likes = None
        self.num_retweets = None
        self.num_responses = None
        self.num_quotes = None
        self.priority = None

    # for pretty printing
    def __str__(self):
        s = ""
        s +=   "id:         " + str(self.id)
        s += "\ntime:       " + str(self.time)
        s += "\nauthor:     " + self.user_display_name + " @" + self.user_at_name
        s += "\n  verified: " + str(self.user_is_verified)
        s += "\n  followers:" + str(self.user_num_followers)
        s += "\nmetrics"
        s += "\n  likes:    " + str(self.num_likes)
        s += "\n  retweets: " + str(self.num_retweets)
        s += "\n  responses:" + str(self.num_responses)
        s += "\n  quotes:   " + str(self.num_quotes)
        s += "\npriority:   " + str(self.priority)
        s += "\ncontent:"
        s += "\n" + self.text
        return s

    # make it possible to iterate over the fields of the object
    # this makes csv export easy
    def __iter__(self):
        for (key, val) in self.__dict__.items():
            if key == "text":
                val = val.replace("\n", "\\n")
            yield val
