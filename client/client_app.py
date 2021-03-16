import json
import os


class ClientCredentials:
    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('SECRET_ID')
        self.redirect_uri = os.getenv('REDIRECT_URL')
