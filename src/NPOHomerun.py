from os import path
from flask import Flask, json


def create_app():
    app = Flask(__name__)

    from . import HDhomerunProxy
    app.register_blueprint(HDhomerunProxy.bp, url_prefix="/")

    from . import NPOstream
    app.register_blueprint(NPOstream.bp)

    return app


