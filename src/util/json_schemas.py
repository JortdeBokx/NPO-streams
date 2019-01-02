from flask import json

streams_config_schema = json.loads("""
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Streams Config Schema",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
          "className": {
            "type": "string",
            "description": "Name of the class that will handle the channels"
          },
          "channels": {
            "type": "array",
            "description": "The list of channels",
            "items": {
              "type": "object",
              "properties": {
                "number":{
                  "type": "number",
                  "minimum": 1,
                  "description": "The channel number to be assigned"
                },
                "name":{
                  "type": "string",
                  "description": "The channel name"
                },
                "key":{
                  "type": "string",
                  "description": "The key that uniquely identifies the channel on the streaming site"
                },
                "enabled":{
                  "type": "boolean",
                  "description": "Whether to list the channel or not"
                }
              },
                "required": [
                  "number",
                  "name",
                  "key",
                  "enabled"
                ]
            }
          }
        },
        "required": [
          "className",
          "channels"
        ]
    }
}
""")
