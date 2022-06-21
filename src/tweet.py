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