import json
import mail
import request

CONFIG_PATH = "config.json"

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

    def get_email_properties(self):
        properties = mail.EMailProperties()
        properties.recipient = self.email_recipient
        properties.authenticate = self.email_authenticate
        properties.smtp_server = self.smtp_server
        properties.port = self.email_server_port
        properties.sender = self.email_sender
        properties.password = self.email_password
        return properties