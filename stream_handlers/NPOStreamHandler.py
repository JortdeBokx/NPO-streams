import logging
import re

import m3u8
import requests

from stream_handlers.BaseStreamHandler import BaseStreamHandler

NPO_IDA_APP_URI = 'https://ida.omroep.nl/app.php/'
NPO_AUTH_URL = "https://ida.omroep.nl/app.php/auth"


class NPOStreamHandler(BaseStreamHandler):
    token = None

    def __init__(self):
        """
        Initialise NPO stream handler by Reading & verifying the config file
        """
        super().__init__()  # Call super init to read config contents
        if not self.config_data:
            raise ValueError("No Configfile was set")

        streams_config = None
        for streamclass in self.config_data:
            if streamclass["className"] == self.__class__.__name__:
                streams_config = streamclass["channels"]

        if not streams_config:
            raise ValueError("NPO stream class not in config data, class name: " + self.__class__.__name__)

        self.streams = [d for d in streams_config]

    def valid_key(self, key):
        try:
            return any(d['key'] == key for d in self.streams)
        except TypeError:
            logging.log('Error', 'Stream variable was not correctly set in NPO Stream Handler')
            return False

    def get_lineup(self, base_url):
        """
        Overwrite function to get lineup object for NPO streams
        :return:
        """
        lineup = []
        try:
            for d in self.streams:
                if d['enabled']:
                    url = base_url + "/" + d['key']
                    lineup.append({'GuideNumber': str(d['number']),
                                   'GuideName': d['name'],
                                   'URL': url
                                   })

            return lineup
        except TypeError:
            logging.log('Error', 'No streams were loaded for NPO streamer, check the streams.json file')
            return []

    def refresh_npo_api_token(self):
        """
        Fetch an API token for the NPO streaming site
        :return:
        """
        try:
            auth_token_json = requests.get(NPO_AUTH_URL).json()
            self.token = auth_token_json["token"]
        except IOError:
            logging.log('Error', 'Could not fetch a token from ' + NPO_AUTH_URL)

    def get_live_m3u8(self, key, quality=0):
        """
        Get's the m3u8 object in the preferred quality
        :param key: The key of the livestream, from streams.json
        :param quality: an integer for the vertical amount of pixels, 0 for maximum quality, invalid -> minimum quality
        :return: an m3u8 object
        """

        m3u8_location = self.get_live_url(key)
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
        else:
            return None

    def get_live_url(self, key):
        """
        Gets the Streaming url of the live stream identified by key
        :param key: The key of the livestream, from streams.json
        :return: URL of the stream
        """

        stream_data = self.get_stream_data(key)
        selected_stream = ""
        if stream_data:
            try:
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
            except KeyError:
                logging.log(logging.ERROR, "Data stream contained no content")
                return None
        else:
            return None

    def get_stream_data(self, key):
        """
        Gets the stream Json
        :param key: The key of the livestream, from streams.json
        :return: Json object with stream data
        """
        if not self.token:
            self.refresh_npo_api_token()
        try:
            data_url, stream_data = self.obtain_stream_url(key)
        except IOError:
            self.refresh_npo_api_token()
            try:
                data_url, stream_data = self.obtain_stream_url(key)
            except IOError:
                logging.log('Error', 'Could not fetch playlist url at ' + data_url)
            return None

        return stream_data

    def obtain_stream_url(self, key):
        data_url = NPO_IDA_APP_URI + key + '?adaptive=no&token=' + self.token
        stream_data = requests.get(data_url).json()
        return data_url, stream_data
