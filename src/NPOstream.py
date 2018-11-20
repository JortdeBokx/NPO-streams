import subprocess
import logging
import time

from os import path
from flask import stream_with_context, Response, Blueprint, abort, request, json
from src.npo import npo

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

    def generate():
        startTime = time.time()
        buffer = []
        Transmitted = False

        stream_url = npo.get_live_m3u8(str(key), quality=0)
        ffmpeg_command = ["ffmpeg", "-i", stream_url, "-c:v", "copy", "-c:a", "copy", "-f", "mpegts",
                          "-preset", "ultrafast",  "-tune", "zerolatency",
                          "-movflags", "faststart", "pipe:stdout"]
        process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1)

        while True:
            data = process.stdout.read(1024)
            buffer.append(data)

            if Transmitted is False and time.time() > startTime + 3 and len(buffer) > 0:
                Transmitted = True

                for i in range(0, len(buffer) - 2):
                    yield buffer.pop(0)

            elif time.time() > startTime + 3 and len(buffer) > 0:
                yield buffer.pop(0)

            process.poll()
            if isinstance(process.returncode, int):
                logging.log('Error', 'FFmpeg has crached')
                break

    return Response(stream_with_context(generate()), mimetype="video/mp2t")
