# twitter-search
A tool to search and prioritize tweets by search term

## Installation
1. install python 3 from <https://www.python.org/> or using a package manager
2. install the following dependencies
    - `jsonpickle`
    - `tweepy`
    - `flask`
    
        All dependencies can be installed by using pip: `pip install -r requirements.txt`
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

### Running in command line mode
If the program is run from the command line (i.e. `./main.py` or `python main.py`) the list of tweets will be updated and given new priorities.
The result will be sent by email if enabled.

### Running the flask server
If the program is run in flask mode, the list of tweets will be updated and given new priorities.
These tweets can be accessed using HTTPS requests and marked as **done** or **undone**. 
For testing, the flask server can be run directly from the command line:
- `export FLASK_APP=main`
- `flask run`
- go to `http://127.0.0.1:5000/tweets` in your web browser

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
send_email | if `true` the result will be sent by e-mail. This also causes the csv file to be exported, even if export_csv is `false`
email_recipient | the e-mail address to send the result to
email_sender | the e-mail address to send the result from
smtp_server | url of the smtp server
email_server_port | port to access the smtp server (numerical value)
email_password | password for the sender address
email_authenticate | if `true` the user is authenticated at the server using the sender address and the password

#### Configuration for KIT smarthost server
To send emails using the KIT smarthost server, you need to be in the KIT network.
If you are not in the KIT network, you can connect to it via VPN.
Use the following settings to connect to the smarthost server:

keyword | value
--- | ---
email_sender | your `kit.edu` email address
smtp_server | `smarthost.kit.edu`
email_server_port | `25`
email_password | is not needed, can be empty
email_authenticate | `false`

For more information see <https://www.scc.kit.edu/dienste/9916.php>
