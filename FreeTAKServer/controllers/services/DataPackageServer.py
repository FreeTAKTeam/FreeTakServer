import logging
import os
import random
import string
import traceback
import xml.etree.ElementTree as ET
from logging.handlers import RotatingFileHandler
from pathlib import Path, PurePath
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.controllers.configuration.SQLcommands import SQLcommands
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.controllers.configuration.DatabaseConfiguration import DatabaseConfiguration

loggingConstants = LoggingConstants()
logger = CreateLoggerController("DataPackageServer").getLogger()
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, send_file
from flask.logging import default_handler

dbController = DatabaseController()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

sql = SQLcommands()
const = DataPackageServerConstants()
log = LoggingConstants()

app = Flask(__name__)  # create the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConfiguration().DataBaseConnectionString
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# TODO: verify session life cycle in dbController doesnt break this logic
dbController.session = db.session
file_dir = os.path.dirname(os.path.realpath(__file__))
dp_directory = PurePath(file_dir, const.DATAPACKAGEFOLDER)

# Set up logging
if not Path(log.LOGDIRECTORY).exists():
    print(f"Creating directory at {log.LOGDIRECTORY}")
    os.makedirs(log.LOGDIRECTORY)
app.logger.removeHandler(default_handler)
formatter = logging.Formatter(log.LOGFORMAT)
file_handler = RotatingFileHandler(
    log.HTTPLOG,
    maxBytes=log.MAXFILESIZE,
    backupCount=log.BACKUPCOUNT
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.ERROR)
#app.logger.addHandler(file_handler)
#console_handler = logging.StreamHandler(sys.stdout)
#console_handler.setFormatter(formatter)
#console_handler.setLevel(logging.DEBUG)
#app.logger.addHandler(console_handler)
#app.logger.setLevel(logging.DEBUG)

@app.route('/')
def hello():
    return 'hello world'

@app.route("/Marti/vcm", methods=[const.GET])
def get_all_video_links():
    # This is called when the user selects the Download button in the Videos window. It
    # expects an XML listing of all known feeds, so the user can pick and choose which ones
    # to store locally
    try:
        feeds = dbController.query_videostream(column=["FullXmlString"])
        app.logger.info(f"Found {len(feeds)} video feeds in {const.DATABASE}")
        if len(feeds) == 0:
            return ("No video feeds found", 500)
        all_feeds = ""
        for feed in feeds:
            # 'feed' is a tuple with one element, so we only append that
            all_feeds += feed.FullXmlString.decode("utf-8")
        return f"<videoConnections>{all_feeds}</videoConnections>"
    except:
        app.logger.error(traceback.format_exc())
        return "Error", 500


@app.route("/Marti/vcm", methods=[const.POST])
def insert_video_link():
    try:
        xml_root = ET.fromstring(request.data.decode("utf-8"))
        for xml_feed in xml_root:
            protocol = xml_feed.find("protocol").text
            alias = xml_feed.find("alias").text
            uid = xml_feed.find("uid").text
            address = xml_feed.find("address").text
            port = xml_feed.find("port").text
            rover_port = xml_feed.find("roverPort").text
            ignore_klv = xml_feed.find("ignoreEmbeddedKLV").text
            preferred_mac = xml_feed.find("preferredMacAddress").text
            path = xml_feed.find("path").text
            buf = xml_feed.find("buffer").text
            timeout = xml_feed.find("timeout").text
            rtsp_reliable = xml_feed.find("rtspReliable").text
            # Check that no other feeds with the same UID have been received
            streams = dbController.query_videostream(query=f'uid == "{uid}"')
            if len(streams) > 0:
                app.logger.info(f"Already received feed with UID={uid} (alias = {alias})")
                continue  # Ignore this feed if there are duplicates
            app.logger.info(f"Inserting video feed into database: {request.data.decode('utf-8')}")
            dbController.create_videostream(FullXmlString = ET.tostring(xml_feed), Protocol = protocol, Alias = alias, uid = uid, Address = address, Port = port, RoverPort=rover_port, IgnoreEmbeddedKlv=ignore_klv, PreferredMacAddress=preferred_mac, Path=path, Buffer=buf, Timeout=timeout, RtspReliable=rtsp_reliable)

        return "Okay", 200
    except:
        app.logger.error(traceback.format_exc())
        return "Error", 500


@app.route('/Marti/api/version/config', methods=[const.GET])
def versionConfig():
    return const.VERSIONJSON


@app.route('/Marti/api/clientEndPoints', methods=[const.GET])
def clientEndPoint():
    return const.versionInfo


@app.route('/Marti/sync/missionupload', methods=[const.POST])
def upload():

    file_hash = request.args.get('hash')
    app.logger.info(f"Data Package hash = {str(file_hash)}")
    letters = string.ascii_letters
    uid = ''.join(random.choice(letters) for i in range(4))
    uid = 'uid-' + str(uid)
    filename = request.args.get('filename')
    creatorUid = request.args.get('creatorUid')
    file = request.files.getlist('assetfile')[0]
    directory = Path(dp_directory, file_hash)
    if not Path.exists(directory):
        os.mkdir(directory)
    file.save(os.path.join(directory, filename))
    fileSize = Path(directory, filename).stat().st_size
    callsign = str(
        FlaskFunctions().getSubmissionUser(creatorUid, dbController))  # fetchone() gives a tuple, so only grab the first element
    FlaskFunctions().create_dp(dbController, uid = uid, Name = filename, Hash = file_hash, SubmissionUser = callsign, CreatorUid = creatorUid, Size = fileSize)
    return IP + ':' + str(HTTPPORT) + "/Marti/api/sync/metadata/" + file_hash + "/tool"


@app.route('/Marti/api/sync/metadata/<hash>/tool', methods=[const.PUT])
def putDataPackageTool(hash):
    if request.data == b'private':
        dbController.update_datapackage(query=f'Hash == "{hash}"', column_value={"Privacy": 1})
    return "Okay", 200


@app.route('/Marti/api/sync/metadata/<hash>/tool', methods=[const.GET])
def getDataPackageTool(hash):
    file_list = os.listdir(str(dp_directory) + '/' + str(hash))
    path = PurePath(dp_directory, str(hash), file_list[0])
    app.logger.info(f"Sending data package from {str(path)}")
    return send_file(str(path))


@app.route('/Marti/sync/search', methods=[const.GET])
def retrieveData():
    keyword = request.args.get('keyword')
    packages = FlaskFunctions().getAllPackages()
    app.logger.info(f"Data packages in the database: {packages}")
    return str(packages)


@app.route('/Marti/sync/content', methods=const.HTTPMETHODS)
def specificPackage():
    hash = request.args.get('hash')
    app.logger.debug(os.listdir(str(dp_directory) + '/' + str(hash)))
    file_list = os.listdir(str(dp_directory) + '/' + str(hash))
    app.logger.debug(const.DATAPACKAGEFOLDER + '\\' + hash + '\\' + file_list[0])
    path = PurePath(dp_directory, str(hash), file_list[0])
    app.logger.debug(str(path))
    return send_file(str(path))


@app.route('/Marti/api/version', methods=[const.GET])
def returnVersion():
    return const.versionInfo


@app.route('/Marti/sync/missionquery', methods=const.HTTPMETHODS)
def checkPresent():
    hash = request.args.get('hash')
    if FlaskFunctions().hashIsPresent(hash, dbController):
        app.logger.info(f"Data package with hash {hash} exists")
        return IP + ':' + str(HTTPPORT) + "/Marti/api/sync/metadata/" + hash + "/tool"
    else:
        app.logger.info(f"Data package with hash {hash} does not exist")
        return '404', 404
    
@app.route('/')
def home():
    return 'data package service is up, good job.'
class FlaskFunctions:

    def __init__(self):
        self.callsigns = []

    def create_dp(self, dbController, **args):
        return dbController.create_datapackage(**args)

    def hashIsPresent(self, hash, dbControl):
        data = dbControl.query_datapackage(query=f'Hash == "{hash}"')
        return len(data) > 0

    def getSubmissionUser(self, UID, dbControl):
        callsign = dbControl.query_user(query=f'uid == "{UID}"', column=['callsign'])
        return callsign

    def getAllPackages(self):
        data = DatabaseController().query_datapackage()
        package_dict = {
            "resultCount": len(data),
            "results": []
        }
        for i in data:
            package_dict["results"].append({
                "UID": i.uid,
                "Name": i.Name,
                "Hash": i.Hash,
                "PrimaryKey": i.PrimaryKey,
                "SubmissionDateTime": str(i.SubmissionDateTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
                "SubmissionUser": i.SubmissionUser,
                "CreatorUid": i.CreatorUid,
                "Keywords": i.Keywords,
                "MIMEType": i.MIMEType,
                "Size": i.Size
            })
        return package_dict

    def startup(self, ip, port):
        try:
            global IP, HTTPPORT
            IP = ip
            HTTPPORT = port
            # Make sure the data package directory exists
            if not Path(dp_directory).exists():
                app.logger.info(f"Creating directory at {str(dp_directory)}")
                os.makedirs(str(dp_directory))
            # Create the relevant database tables
            print(const.IP)
            print(HTTPPORT)
            app.run(host= ip, port=HTTPPORT, debug=const.HTTPDEBUG)
        except Exception as e:
            logger.error('there has been an exception in Data Package service startup ' + str(e))
            return -1

    def stop(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

if __name__ == "__main__":
    pass

