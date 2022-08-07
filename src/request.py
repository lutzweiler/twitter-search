import time
import tweepy
import tweet

# this class contains the settings for making requests using the twitter api
class RequestProperties:
    def __init__(self):
        self.bearer_token = None
        self.max_results = 100
        self.search_terms = None #List of search terms, joined with OR
        self.language_identifier = "de"
        self.request_delay = 2 #number of seconds to wait between request pages
        self.time_cutoff = None

# this class makes search requests to twitter using the search_recent endpoint
# the twiter response comes in multiple pages. we aggregate all responses into
# a single list and convert the json data to tweet objects
class TwitterRequest:
    def __init__(self, properties):
        self.properties = properties
        self.query = None
        self.result = []
        self.tweepy_client = tweepy.Client(self.properties.bearer_token)
        self.build_query()
    
    # combine all search terms from the configuration into a single query
    def build_query(self):
        query = "("
        query += " OR ".join(self.properties.search_terms)
        query += ")"
        query += " lang:" + self.properties.language_identifier
        self.query = query

    # makes requests to the twitter api and converts the result
    def execute(self):
        print("starting request with query:", self.query)
        tweets_per_page = 100
        tweet_count = 0
        next_token = None

        #a helper function to get the user from an id
        #this is needed because the user data is not directly included in a tweet but
        #instead sent in a seperate object
        def find_user(includes, user_id):
            for user in includes['users']:
                if user.id == user_id:
                    return user
            return None

        # iterate over (possibly) multiple pages of results
        while tweet_count < self.properties.max_results:
            num_tweets = min(tweets_per_page, self.properties.max_results - tweet_count)
            if num_tweets < 10: #the API requires at least ten tweets
                num_tweets = 10

            print("-loading", num_tweets, "tweets")
            # make the request
            response = self.tweepy_client.search_recent_tweets(
                self.query,
                max_results = num_tweets,
                expansions = "author_id",
                tweet_fields = "id,text,author_id,created_at,public_metrics",
                user_fields = "id,username,public_metrics,verified",
                next_token = next_token
            )
            data, includes, errors, meta = response
            if data == None:
                print("-no more results found")
                break


            # if there is no error, generate tweet objects from the result
            if errors == []:
                for t in data:
                    # end request if tweets are too old
                    if self.properties.time_cutoff != None:
                        if t.created_at <= self.properties.time_cutoff:
                            break

                    new_tweet = tweet.Tweet()
                    user = find_user(includes, t.author_id)
                    new_tweet.id = t.id
                    new_tweet.time = t.created_at
                    new_tweet.text = t.text
                    new_tweet.user_at_name = user.username
                    new_tweet.user_display_name = user.name
                    new_tweet.user_num_followers = user.public_metrics['followers_count']
                    new_tweet.user_is_verified = user.verified
                    new_tweet.num_likes = t.public_metrics['like_count']
                    new_tweet.num_retweets = t.public_metrics['retweet_count']
                    new_tweet.num_responses = t.public_metrics['reply_count']
                    new_tweet.num_quotes = t.public_metrics['quote_count']
                    new_tweet.done = False
                    self.result.append(new_tweet)
            else: 
                print("an error has occured")
                print(errors)

            next_token = meta['next_token']
            tweet_count += len(data)
            
            if tweet_count < self.properties.max_results:
                print("-waiting", self.properties.request_delay, "seconds")
                time.sleep(self.properties.request_delay)

    def get_result(self):
        return self.result
