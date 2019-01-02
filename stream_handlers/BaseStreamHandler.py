import collections
import json
from os import path

import jsonschema

from util import json_schemas


class BaseStreamHandler:
    config_path = path.abspath(
        path.join(path.dirname(path.dirname(__file__)), "config",
                  "streams.json"))  # ../config/streams.json

    def __init__(self):
        # Validate config layout
        with open(self.config_path, 'r') as streams:
            config_data = json.load(streams)

        jsonschema.validate(config_data, json_schemas.streams_config_schema)

        channel_numbers = []
        for channel_Set in config_data:
            for channel in channel_Set["channels"]:
                channel_numbers.append(channel["number"])

        doubles = [item for item, count in collections.Counter(channel_numbers).items() if count > 1]
        if doubles:
            raise ValueError(
                "Duplicate channel numbers detected! Please check the channel config file for the following "
                "duplicates channel numbers: " + doubles.__str__())
        self.config_data = config_data


def get_lineup(self, base_url):
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
            "description": "The URL where the stream can be viewed, base_url + some extension"
          }
        },
        "required": [
          "GuideName", "GuideNumber", "URL"
        ]
      }
    }
    :return: Array of available channels in json format according to above JSON schema
    """
    raise NotImplementedError("Please Implement this method")


def get_live_m3u8(self, key, quality=0):
    """
    Gets a m3u8 url for the stream at of channel key with set quality
    :param key: the key of the channel
    :param quality: an integer for the vertical amount of pixels, 0 for maximum quality, invalid -> minimum quality
    :return:
    """
    raise NotImplementedError("Please Implement this method")


def valid_key(self, key):
    """
    Validates a key
    :param key: key to be validated
    :return:
    """
    raise NotImplementedError("Please Implement this method")
