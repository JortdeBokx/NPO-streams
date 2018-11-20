import logging

from os import path
from flask import stream_with_context, Response, Blueprint, abort, request, json
from src.npo import npo
from .Helpers import generate_stream_ffmpeg

URL_PREFIX = "NPOstream"

bp = Blueprint('NPOstream', __name__, url_prefix="/" + URL_PREFIX)


def valid_key(key):
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "npo", "streams.json"))
    try:
        with open(filepath, 'r') as streams:
            stream_json = json.load(streams)
            return any(d['key'] == key for d in stream_json)
    except EnvironmentError:
        logging.log('Error', 'Reading streams.json file failed. Make sure it is present in the npo directory, '
                             'and of the correct format')
        return False


def get_lineup():
    return npo.get_lineup(request.host_url + URL_PREFIX)


@bp.route('/<key>')
def stream_stuff(key):
    if not valid_key(key):
        abort(404)

    stream_url = npo.get_live_m3u8(str(key), quality=0)

    return Response(stream_with_context(generate_stream_ffmpeg(stream_url)), mimetype="video/mp2t")
