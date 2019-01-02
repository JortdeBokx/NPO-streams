import logging

import requests

from src.stream_handlers.BaseStreamHandler import BaseStreamHandler, Stream

NPO_AUTH_URL = "https://ida.omroep.nl/app.php/auth"
NPO_CONFIG_CLASS_NAME = "NPOStreamHandler"  # Class name to filter by in config name


class NPOStreamHandler(BaseStreamHandler):
    token = None

    def __init__(self):
        """
        Initialise NPO stream handler by doing the following steps:
        - Read & verify config file
        - get the stream tokens and stuff
        """
        super().__init__()  # Call super init to read config contents
        if not self.config_data:
            raise ValueError("No Configfile was set")

        for streamclass in self.config_data:
            if streamclass["className"] == NPO_CONFIG_CLASS_NAME:
                streams_config = streamclass["channels"]

        if not streams_config:
            raise ValueError("NPO stream class not in config data, class name:" + NPO_CONFIG_CLASS_NAME)

        self.streams = [Stream(name=d["name"], number=d["number"], key=d["key"]) for d in streams_config]

        self.refresh_npo_api_token()

    def get_lineup(self):
        """
        Overwrite function to get lineup object for NPO streams
        :return:
        """

    def refresh_npo_api_token(self):
        try:
            auth_token_json = requests.get(NPO_AUTH_URL).json()
            self.token = auth_token_json["token"]
        except IOError:
            logging.log('Error', 'Could not fetch a token from ' + NPO_AUTH_URL)
