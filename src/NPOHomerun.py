from os import path
from flask import Flask, json


def create_app():
    app = Flask(__name__)

    from . import HDhomerunProxy
    app.register_blueprint(HDhomerunProxy.bp, url_prefix="/")

    from . import NPOstream
    app.register_blueprint(NPOstream.bp)

    return app


if __name__ == '__main__':
    config = {}
    try:
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "config.json"))
        config = json.load(open(filepath, 'r'))
    except FileNotFoundError:
        print("Error with configuration file, file not found")
        exit(0)

    app = create_app()
    app.run(host=config["bindAddr"], port=config["port"])
