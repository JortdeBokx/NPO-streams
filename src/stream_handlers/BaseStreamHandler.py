import json
from os import path

import jsonschema

from src.util import json_schemas


class BaseStreamHandler:
    config_path = path.abspath(
        path.join(path.dirname(path.dirname(path.dirname(__file__))), "config",
                  "streams.json"))  # ../../config/streams.json

    def __init__(self):
        # Validate config layout
        with open(self.config_path, 'r') as streams:
            config_data = json.load(streams)

        jsonschema.validate(config_data, json_schemas.streams_config_schema)

        self.config_data = config_data

    def get_lineup(self):
        """
        Creates a lineup of available channels in a json object. It should have the following JSON schema:
        {
          "$schema": "http://json-schema.org/draft-07/schema#",
          "title": "Lineup Data",
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "GuideName": {
                "type": "string",
                "description": "The display name of the channel"
              },
              "GuideNumber": {
                "type": "string",
                "pattern": "^[1-9][0-9]*",
                "description": "The display number"
              },
              "URL": {
                "type": "string",
                "format": "URI",
                "description": "The URL where the stream can be viewed"
              }
            },
            "required": [
              "loc"
            ]
          }
        }
        :return: Array of available channels in json format according to above JSON schema
        """
        raise NotImplementedError("Please Implement this method")


class Stream:
    def __init__(self, name, number, key):
        self.name = name
        self.number = number
        self.key = key
