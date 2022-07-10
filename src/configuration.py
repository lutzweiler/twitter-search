import json
import request

CONFIG_PATH = "config.json"

class Configuration:
    def __init__(self, bearer_token, search_terms, max_results, language_identifier, request_delay, export_csv, csv_path, send_email, email_recipient):
        self.bearer_token = bearer_token
        self.search_terms = search_terms
        self.max_results = max_results
        self.language_identifier = language_identifier
        self.request_delay = request_delay
        self.export_csv = export_csv
        self.csv_path = csv_path
        self.send_email = send_email
        self.email_recipient = email_recipient

    @staticmethod
    def load_config_file():
        with open(CONFIG_PATH, 'r') as f:
            s = f.read()
        j = json.loads(s)
        c = Configuration(**j)
        return c

    def get_request_properties(self):
        properties = request.RequestProperties()
        properties.bearer_token = self.bearer_token
        properties.search_terms = self.search_terms
        properties.max_results = self.max_results
        properties.language_identifier = self.language_identifier
        properties.request_delay = self.request_delay
        return properties
