from os import path

from flask import Flask

from src.stream_handlers.NPOStreamHandler import NPOStreamHandler
from . import HDhomerunProxy

app = Flask(__name__)
app.config["DEBUG"] = False
app.config["PORT"] = 5004
app.config["HOST"] = "127.0.0.1"

app.config.from_json(path.abspath(
    path.join(path.dirname(path.dirname(__file__)), "config",
              "config.json")))  # ../config/config.json

stream_handlers = []
npo = NPOStreamHandler()
stream_handlers.append(npo)

HDhomerunProxy.setup_hdhrproxy(app, stream_handlers)

app.run(host=app.config["HOST"], port=app.config["PORT"])
