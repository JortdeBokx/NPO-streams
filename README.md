# NPO-streams
Fetches Live tv streams from all Dutch public broadcast channels (Nederlandse Publieke Omroep), and re-streams them, whilst also providing an HDHomerun emulation for use in Emby or Plex.
The Proxy runs as a small flask app.

I made this application as I watch tv very rarely, and when I do don't want to use the npo website. Using this service you can stream the following channels:
*  NPO 1,2,3
*  NPO 1,2,3 extra
*  NPO nieuws
*  NPO politiek
*  NPO Radio 1,2,3,4 webcams

More chanels could be added later. The channels are retransmitted as if they came from an HDHomerun, which is a commonly used cable tv rebroadcaster for which Emby and Plex have good support.

## Installation
I recommend using pipenv to install the required dependencies;

1.  Make sure you have pip installed, on ubuntu/debian install with `apt install python-pip`
2.  Make sure you have FFMPEG installed, see https://www.ffmpeg.org/download.html for more information 
2.  Install pipenv `pip install pipenv`
3.  Clone this repo into a directory `git clone https://github.com/JortdeBokx/NPO-streams.git`, you can also download and unpack the zip
4.  Change directory to the downloaded folder `cd NPO-streams`
5.  Create a pipenv usign `pipenv --python3.6` (you can also use python3.7)
6.  Install the dependencies usign `pipenv install`
7.  Copy the template configuration files using `cp config/config.json.default config/config.json` and `cp config/channels.json.default config/channels.json`
8.  You can verify the app works by running `pipenv run python npo-streams.py`, if you go to `localhost:5004` you should get a response from the server.

If you want to run NPO streams as a systemd service, I included a template service file.
You should edit this file such that the paths match the installation location. 
After that copy the file to `/etc/systemd/system/` and run `systemctl enable NPOstreams.service` to enable the service on startup

In Emby or Plex you can now add a new tv tuner by entering the ip of the proxy as well as the port.

## Configuration
The configuration is split into 2 files

### config.json
This file contains the general configuration of the flask app. Any flask configuration entries can be placed here, see [the flask documentation](http://flask.pocoo.org/docs/1.0/config/) for more info
You can change the port and host to allow access from outside the machine.

You can also specify a quality number, this number can be 0 for the maximum quality, or an amount of vertical pixels, if that amount is available (see the gear icon on the npo player for avaiable qualities)

### channels.json
This file contains all the channels available. They are grouped by the class name of the stream handler that handle's their streams (this is to allow future expandibility)
Each channel consists of 4 attrbutes: a number (this must be unique), a name, a key (unique identification for streaming service) and a flag to enable/disable specific channels.

## Contributing
I very happily accept contributions to this project, 
A lot can be done to improve the overal structure and add new features such as EPG, channel logos, etc...
Please check the [Contributing Guidelines](https://github.com/JortdeBokx/NPO-streams/blob/master/CONTRIBUTING.md) for more information.

## License
All content is released under the MIT license, see [LICENSE](https://github.com/JortdeBokx/NPO-streams/blob/master/LICENSE) for more information.

## Help needed
If you need any help installing/running/configuring/altering this project don't hesitate to contact me by creating an issue, or sending me an email.

