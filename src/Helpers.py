import subprocess
import time
import logging


def generate_stream_ffmpeg(stream_url):
    startTime = time.time()
    buffer = []
    Transmitted = False

    # TODO: make this smoother and better in all ways
    # Look at how tvheadend does it
    # https://trac.ffmpeg.org/wiki/StreamingGuide

    ffmpeg_command = ["ffmpeg",
                      "-i", stream_url,
                      "-c:v", "copy",
                      "-c:a", "copy",
                      "-f", "mpegts",
                      "-preset", "ultrafast",
                      "-blocksize", "1024",
                      # "-tune", "zerolatency",
                      # "-movflags", "faststart",
                      "pipe:stdout"]
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
