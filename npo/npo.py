import requests, re


def get_live_url(key):
    """
    Gets the Streaming url of the live stream identified by key
    :param key: The key of the livestream, from streams.json
    :return: URL of the stream
    """

    stream_data = get_stream_data(key)
    print(stream_data)
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
            print(stream_url)


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

get_live_url("LI_NL1_4188102")