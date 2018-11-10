import subprocess
import time
import json

from os import path
from flask import stream_with_context, Response, Blueprint, abort, request
from src.npo import npo

URL_PREFIX = "NPOstream"

bp = Blueprint('NPOstream', __name__, url_prefix="/" + URL_PREFIX)


def valid_key(key):
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "npo", "streams.json"))
    with open(filepath, 'r') as streams:
        stream_json = json.load(streams)
        return any(d['key'] == key for d in stream_json)


def get_lineup():
    return npo.get_lineup(request.host_url + URL_PREFIX)


@bp.route('/<key>')
def stream_stuff(key):
    if not valid_key(key):
        abort(404)

    def generate():
        startTime = time.time()
        buffer = []
        sentBurst = False

        stream_url = npo.get_live_m3u8(str(key), quality=0)
        ffmpeg_command = ["ffmpeg", "-i", stream_url, "-c:v", "copy", "-c:a", "copy", "-f", "mpegts",
                          "-movflags", "faststart", "pipe:stdout"]
        process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1)

        while True:
            # Get some data from ffmpeg
            line = process.stdout.read(1024)

            # We buffer everything before outputting it
            buffer.append(line)

            # Minimum buffer time, 3 seconds
            if sentBurst is False and time.time() > startTime + 3 and len(buffer) > 0:
                sentBurst = True

                for i in range(0, len(buffer) - 2):
                    yield buffer.pop(0)

            elif time.time() > startTime + 3 and len(buffer) > 0:
                yield buffer.pop(0)

            process.poll()
            if isinstance(process.returncode, int):
                break

    return Response(stream_with_context(generate()), mimetype="video/mp2t")

