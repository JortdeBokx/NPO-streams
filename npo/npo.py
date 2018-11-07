import requests, re, m3u8


def get_live_m3u8(key, quality=0):
    """
    Get's the m3u8 object in the preferred quality
    :param key: The key of the livestream, from streams.json
    :param quality: an integer where lower = best quality. every 1 value higher means a lower quality
    :return: an m3u8 object
    """

    m3u8_location = get_live_url(key)
    print(m3u8_location)
    if m3u8_location:
        m3u8_obj = m3u8.load(m3u8_location)
        Base_URI = m3u8_obj.base_uri

        if m3u8_obj.is_variant:
            for m3u8_playlist in m3u8_obj.playlists:
                print(m3u8_playlist)
        else:
            # TODO: if no playlists then get stream instantly
            pass

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
    Gets the stream Blob used to play the stream
    :param key: The key of the livestream, from streams.json
    :return: Json object with stream data
    """
    auth_token_json = requests.get('https://ida.omroep.nl/app.php/auth').json()
    token = auth_token_json["token"]

    data_url = 'https://ida.omroep.nl/app.php/' + key + '?adaptive=no&token=' + token
    stream_data = requests.get(data_url).json()

    return stream_data


get_live_m3u8("LI_NL1_4188102")