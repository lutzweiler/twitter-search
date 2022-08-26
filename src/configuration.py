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

import json
import mail
import request

# path where we expect the config file to be, relative to main.py
CONFIG_PATH = "config.json"

# this class contains the configuration data for the application
class Configuration:
    def __init__(self, bearer_token, search_terms, max_results, language_identifier,
        request_delay, export_csv, csv_path, send_email, email_recipient, email_sender,
        smtp_server, email_server_port, email_password, email_authenticate):
        self.bearer_token = bearer_token
        self.search_terms = search_terms
        self.max_results = max_results
        self.language_identifier = language_identifier
        self.request_delay = request_delay
        self.export_csv = export_csv
        self.csv_path = csv_path
        self.send_email = send_email
        self.email_recipient = email_recipient
        self.email_sender = email_sender
        self.smtp_server = smtp_server
        self.email_server_port = email_server_port
        self.email_password = email_password
        self.email_authenticate = email_authenticate

    # creates a Configuration object from a configuration file
    # this does not test whether all relevant fields exist and are set
    @staticmethod
    def load_config_file():
        with open(CONFIG_PATH, 'r') as f:
            s = f.read()
        j = json.loads(s)
        c = Configuration(**j)
        return c

    # return the relevant settings for accessing the twitter api and
    # making search requests
    def get_request_properties(self):
        properties = request.RequestProperties()
        properties.bearer_token = self.bearer_token
        properties.search_terms = self.search_terms
        properties.max_results = self.max_results
        properties.language_identifier = self.language_identifier
        properties.request_delay = self.request_delay
        return properties

    # return the relevant settings for sending email
    def get_email_properties(self):
        properties = mail.EMailProperties()
        properties.recipient = self.email_recipient
        properties.authenticate = self.email_authenticate
        properties.smtp_server = self.smtp_server
        properties.port = self.email_server_port
        properties.sender = self.email_sender
        properties.password = self.email_password
        return properties
