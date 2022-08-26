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
        self.done = None

    def from_argument_list(self, _id, time, text, user_at_name, user_display_name, user_num_followers, user_is_verified, num_likes, num_retweets, num_responses, num_quotes, priority, done):
        self.id = _id
        self.time = time
        self.text = text
        self.user_at_name = user_at_name
        self.user_display_name = user_display_name
        self.user_num_followers = user_num_followers
        self.user_is_verified = user_is_verified
        self.num_likes = num_likes
        self.num_retweets = num_retweets
        self.num_responses = num_responses
        self.num_quotes = num_quotes
        self.priority = priority
        self.done = done


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
        s += "\ndone:       " + str(self.done)
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
