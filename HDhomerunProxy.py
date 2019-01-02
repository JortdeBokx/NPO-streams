import logging

from flask import jsonify, request, abort, Response, stream_with_context

# Code similar to https://github.com/jkaberg/tvhProxy
from util.Helpers import generate_stream_ffmpeg


def setup_hdhrproxy(app, stream_handlers):
    lineup = []
    for sh in stream_handlers:
        name = sh.__class__.__name__
        lineup += sh.get_lineup("http://" + app.config["HOST"] + ":" + str(app.config["PORT"]) + "/" + name)

    logging.info('Lineup: ' + str(lineup))

    @app.route('/<class_name>/<key>')
    def stream_stuff(class_name, key):
        sh = None
        for i in stream_handlers:
            if i.__class__.__name__ == class_name:
                sh = i
        if not sh:
            abort(404)
        if not sh.valid_key(key):
            abort(404)

        stream_url = sh.get_live_m3u8(str(key), quality=app.config["QUALITY"])
        if not stream_url:
            logging.error("Could not get stream url")
            abort(404)
        return Response(stream_with_context(generate_stream_ffmpeg(stream_url)), mimetype="video/mp2t")

    @app.route('/discover.json')
    def discover():
        discover_data = {
            'FriendlyName': 'NPOproxy',
            'Manufacturer': 'Silicondust',
            'ModelNumber': 'HDTC-2US',
            'FirmwareName': 'hdhomeruntc_atsc',
            'TunerCount': 1,
            'FirmwareVersion': '20150826',
            'DeviceID': '12345678',
            'DeviceAuth': 'test1234',
            'BaseURL': '%s' % request.host_url,
            'LineupURL': '%slineup.json' % request.host_url
        }
        return jsonify(discover_data)

    @app.route('/lineup_status.json')
    def status():
        return jsonify({
            'ScanInProgress': 0,
            'ScanPossible': 1,
            'Source': "Cable",
            'SourceList': ['Cable']
        })

    @app.route('/lineup.json')
    def give_lineup():
        return jsonify(lineup)

    @app.route('/lineup.post', methods=['GET', 'POST'])
    def lineup_post():
        return ''

    @app.route('/')
    @app.route('/device.xml')
    def device():
        discover_data = {
            'FriendlyName': 'NPOproxy',
            'Manufacturer': 'Silicondust',
            'ModelNumber': 'HDTC-2US',
            'FirmwareName': 'hdhomeruntc_atsc',
            'TunerCount': 1,
            'FirmwareVersion': '20150826',
            'DeviceID': '12345678',
            'DeviceAuth': 'test1234',
            'BaseURL': '%s' % request.host_url,
            'LineupURL': '%slineup.json' % request.host_url
        }

        return """
        <root xmlns="urn:schemas-upnp-org:device-1-0">
        <specVersion>
            <major>1</major>
            <minor>0</minor>
        </specVersion>
        <URLBase>""" + discover_data["BaseURL"] + """"</URLBase>
        <device>
            <deviceType>urn:schemas-upnp-org:device:MediaServer:1</deviceType>
            <friendlyName>""" + discover_data["FriendlyName"] + """"</friendlyName>
            <manufacturer>""" + discover_data["Manufacturer"] + """"</manufacturer>
            <modelName>""" + discover_data["ModelNumber"] + """"</modelName>
            <modelNumber>""" + discover_data["ModelNumber"] + """"</modelNumber>
            <serialNumber></serialNumber>
            <UDN>uuid:""" + discover_data["DeviceID"] + """"</UDN>
        </device>
    </root>
        """, {'Content-Type': 'application/xml'}
