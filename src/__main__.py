from flask import Flask
from . import HDhomerunProxy, NPOstream

app = Flask(__name__)

app.register_blueprint(HDhomerunProxy.bp, url_prefix="/")
app.register_blueprint(NPOstream.bp)

