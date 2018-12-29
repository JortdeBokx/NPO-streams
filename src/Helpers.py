import os
import subprocess


def generate_stream_ffmpeg(stream_url):
    ffmpeg_command = ["ffmpeg",
                      "-i", stream_url,
                      "-c:v", "copy",
                      "-c:a", "copy",
                      "-f", "mpegts",
                      # "-preset", "ultrafast",
                      # "-blocksize", "1024",
                      # "-tune", "zerolatency",
                      # "-movflags", "faststart",
                      "pipe:stdout"]
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
    try:
        f = process.stdout
        byte = f.read(512)
        while True:
            yield byte
            byte = f.read(512)

    except Exception:
        print("An Exception occurred with ffmpeg")
        process.kill()
    finally:
        process.kill()
