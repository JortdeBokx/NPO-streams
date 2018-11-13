import json
from os import path

import m3u8
import re
import requests


def get_live_m3u8(key, quality=0):
    """
    Get's the m3u8 object in the preferred quality
    :param key: The key of the livestream, from streams.json
    :param quality: an integer for the vertical amount of pixels, 0 for maximum quality, invalid -> minimum quality
    :return: an m3u8 object
    """

    m3u8_location = get_live_url(key)
    if m3u8_location:
        m3u8_obj = m3u8.load(m3u8_location)
        Base_URI = m3u8_obj.base_uri

        if m3u8_obj.is_variant:
            options = {}
            for m3u8_playlist in m3u8_obj.playlists:
                resolution = m3u8_playlist.stream_info.resolution
                if resolution:  # If we don't have the audio-only stream
                    options[str(resolution[1])] = Base_URI + m3u8_playlist.uri

            if quality == 0:
                preferred_m3u8_url = options[str(max(options, key=int))]  # int refers to function int()
            else:
                try:
                    preferred_m3u8_url = options[str(quality)]
                except KeyError:
                    preferred_m3u8_url = options[str(min(options, key=int))]
            return preferred_m3u8_url
        else:
            return m3u8_obj.uri


def get_live_url(key):
    """
    Gets the Streaming url of the live stream identified by key
    :param key: The key of the livestream, from streams.json
    :return: URL of the stream
    """

    stream_data = get_stream_data(key)
    selected_stream = ""
    if stream_data:
        for streams in stream_data['items']:
            for stream in streams:
                if stream['contentType'] == "live":
                    selected_stream = stream['url']
                    break
        if selected_stream:
            stream_url = requests.get(selected_stream).text
            stream_url = stream_url.split('"')[1]
            stream_url = re.sub(r"\\", '', stream_url)
            return stream_url


def get_stream_data(key):
    """
    Gets the stream Json
    :param key: The key of the livestream, from streams.json
    :return: Json object with stream data
    """
    auth_token_json = requests.get('https://ida.omroep.nl/app.php/auth').json()
    token = auth_token_json["token"]

    data_url = 'https://ida.omroep.nl/app.php/' + key + '?adaptive=no&token=' + token
    stream_data = requests.get(data_url).json()

    return stream_data


def get_lineup(base_url):
    """
    Returns a JSON object with the channels, and where to get them, similar to HDHomerun
    :param base_url: The base url for any streaming
    :return:
    """
    lineup = []
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "streams.json"))
    with open(filepath, 'r') as streams:
        stream_json = json.load(streams)
        for d in stream_json:
            if d['enabled']:
                url = base_url + "/" + d['key']
                lineup.append({'GuideNumber': str(d['number']),
                               'GuideName': d['name'],
                               'URL': url
                               })
    return lineup
