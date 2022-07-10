# twitter-search
A tool to search and prioritize tweets by search term

## Installation
1. install python 3 from <https://www.python.org/> or using a package manager
2. install the dependencies following dependencies
    - `jsonpickle`
    - `tweepy`
    
        All dependencies can be installed by using pip: `pip install jsonpickle tweepy
3. clone this repository

## Accessing the Twitter API
Using this application requires a Twitter Developer Account. 
A free account can be created at <https://developer.twitter.com>.
The essential access API level is sufficient.

After account creation take the following steps:
1. create a new project
2. within that project, create a new app
3. select "keys and tokens" in the top bar
4. generate the bearer token and copy it to the configuration file

## How to Use

### Configuration
The settings for the application can be changed in the configuration file `src/config.json`

Explanation of the individual settings:
keyword | meaning
--- | ---
bearer_token | a string used to access the twitter API (see above)
search_terms | a list of strings of search terms. Tweets that match any of the search terms will be included in the result
max_results | maximum number of tweets to be retrieved
language_identifier | string representing the required language. See [lang tag here](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query#list)
request_delay | number of seconds to wait inbetween individual requests. Every 100 tweets require an individual request. If the delay is too small, Twitter may timeout the IP. Default value: `2`
export_csv | if `true` the result gets exported in a `.csv` file
csv_path | the path and filename of the csv export
send_email | if `true` the result will be sent by e-mail
email_recipient | the e-mail adress to send the result to

