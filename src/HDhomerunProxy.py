from flask import Blueprint, jsonify, request

from .NPOstream import get_lineup as get_npo_lineup

bp = Blueprint('HDHomerunProxy', __name__)


# Code similar to https://github.com/jkaberg/tvhProxy

@bp.route('/discover.json')
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


@bp.route('/lineup_status.json')
def status():
    return jsonify({
        'ScanInProgress': 0,
        'ScanPossible': 1,
        'Source': "Cable",
        'SourceList': ['Cable']
    })


@bp.route('/lineup.json')
def lineup():
    lineup = []
    lineup += get_npo_lineup()
    return jsonify(lineup)


@bp.route('/lineup.post', methods=['GET', 'POST'])
def lineup_post():
    return ''


@bp.route('/')
@bp.route('/device.xml')
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
