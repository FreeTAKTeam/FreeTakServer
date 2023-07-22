"""this module is responsible for running the DataPackage service
as it utilizes flask, each method represents an endpoint
this web server is responsible for all HTTP queries to
FTS from an ATAK client"""
import logging
import os
import random
import string
import traceback
import defusedxml.ElementTree as ET
from logging.handlers import RotatingFileHandler
from pathlib import Path, PurePath
from FreeTAKServer.core.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.core.configuration.SQLcommands import SQLcommands
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.persistence.DatabaseController import DatabaseController
from FreeTAKServer.core.configuration.DatabaseConfiguration import DatabaseConfiguration
from FreeTAKServer.components.extended.excheck.controllers.ExCheckController import ExCheckController
import eventlet
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, send_file, escape
from flask.logging import default_handler
from werkzeug.utils import secure_filename

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()


loggingConstants = LoggingConstants(log_name="FTS-DataPackage_Service")
logger = CreateLoggerController("FTS-DataPackage_Service", logging_constants=loggingConstants).getLogger()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

USINGSSL = False
ALLOWED_EXTENSIONS = set(['zip'])

sql = SQLcommands()
const = DataPackageServerConstants()
log = LoggingConstants()

app = Flask(__name__)  # create the Flask app
config = MainConfig.instance()
app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConfiguration().DataBaseConnectionString
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = config.SecretKey
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
# TODO: verify session life cycle in dbController doesnt break this logic
# Set up logging
app.logger.removeHandler(default_handler)  # pylint: disable=no-member; member does exist
formatter = logging.Formatter(log.LOGFORMAT)
file_handler = RotatingFileHandler(
    log.HTTPLOG,
    maxBytes=log.MAXFILESIZE,
    backupCount=log.BACKUPCOUNT
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.ERROR)


# app.logger.addHandler(file_handler)
# console_handler = logging.StreamHandler(sys.stdout)
# console_handler.setFormatter(formatter)
# console_handler.setLevel(logging.DEBUG)
# app.logger.addHandler(console_handler)
# app.logger.setLevel(logging.DEBUG)

#TODO Change everything about this
def init_config():
    global dbController, dp_directory

    dbController = DatabaseController()
    dbController.session = db.session

    dp_directory = config.DataPackageFilePath

    if not Path(dp_directory).exists():
        app.logger.info(f"Creating directory at {str(dp_directory)}")
        os.makedirs(str(dp_directory))

    if not os.path.exists(config.ExCheckMainPath):
        os.mkdir(config.ExCheckMainPath)

    if not os.path.exists(config.ExCheckChecklistFilePath):
        os.mkdir(config.ExCheckChecklistFilePath)

    if not os.path.exists(config.ExCheckFilePath):
        os.mkdir(config.ExCheckFilePath)

@app.route('/')
def hello():
    return 'hello world'


@app.route('/Alive')
def alive():
    return 'DataPackage service alive', 200


@app.route("/Marti/vcm", methods=[const.GET])
def get_all_video_links():
    # This is called when the user selects the Download button in the Videos window. It
    # expects an XML listing of all known feeds, so the user can pick and choose which ones
    # to store locally
    try:
        feeds = dbController.query_videostream(column=["FullXmlString"])
        app.logger.info(
            f"Found {len(feeds)} video feeds in {const.DATABASE}")  # pylint: disable=no-member; member does exist
        if len(feeds) == 0:
            return ("No video feeds found", 500)
        all_feeds = ""
        for feed in feeds:
            # 'feed' is a tuple with one element, so we only append that
            all_feeds += feed.FullXmlString.decode("utf-8")
        return f"<videoConnections>{all_feeds}</videoConnections>"
    except:
        app.logger.error(traceback.format_exc())  # pylint: disable=no-member; member does exist
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
            streams = dbController.query_videostream(query=f'uid = "{uid}"')
            if len(streams) > 0:
                app.logger.info(
                    f"Already received feed with UID={uid} (alias = {alias})")  # pylint: disable=no-member; member does exist
                continue  # Ignore this feed if there are duplicates
            app.logger.info(
                f"Inserting video feed into database: {request.data.decode('utf-8')}")  # pylint: disable=no-member; member does exist
            dbController.create_videostream(FullXmlString=ET.tostring(xml_feed), Protocol=protocol, Alias=alias,
                                            uid=uid, Address=address, Port=port, RoverPort=rover_port,
                                            IgnoreEmbeddedKlv=ignore_klv, PreferredMacAddress=preferred_mac, Path=path,
                                            Buffer=buf, Timeout=timeout, RtspReliable=rtsp_reliable)

        return "Okay", 200
    except:
        app.logger.error(traceback.format_exc())
        return "Error", 500


@app.route('/Marti/api/version/config', methods=[const.GET])
def versionConfig():
    logger.info('sending client version json')
    return const.VERSIONJSON


@app.route('/Marti/api/clientEndPoints', methods=[const.GET])
def clientEndPoint():
    logger.info('sending client version info')
    return const.versionInfo


@app.route('/Marti/sync/missionupload', methods=[const.POST])
def upload():
    from FreeTAKServer.model.ServiceObjects.SSLDataPackageVariables import SSLDataPackageVariables
    logger.info('datapackage upload started')
    file_hash = sanitize_hash(request.args.get('hash'))
    app.logger.info(f"Data Package hash = {str(file_hash)}")
    letters = string.ascii_letters
    uid = ''.join(random.choice(letters) for i in range(4))
    uid = 'uid-' + str(uid)
    filename = secure_filename(request.args.get('filename'))
    creatorUid = request.args.get('creatorUid')
    file = request.files.getlist('assetfile')[0]
    directory = Path(dp_directory, file_hash)
    if not Path.exists(directory):
        os.mkdir(str(directory))
    file.save(os.path.join(str(directory), filename))
    fileSize = Path(str(directory), filename).stat().st_size
    callsign = str(
        FlaskFunctions().getSubmissionUser(creatorUid,
                                           dbController))  # fetchone() gives a tuple, so only grab the first element
    FlaskFunctions().create_dp(dbController, uid=uid, Name=filename, Hash=file_hash, SubmissionUser=callsign,
                               CreatorUid=creatorUid, Size=fileSize)
    if USINGSSL == False:
        return "http://" + IP + ':' + str(HTTPPORT) + "/Marti/api/sync/metadata/" + file_hash + "/tool"

    else:
        return "https://" + IP + ':' + str(HTTPPORT) + "/Marti/api/sync/metadata/" + file_hash + "/tool"


@app.route('/Marti/api/sync/metadata/<hash>/tool', methods=[const.PUT])
def putDataPackageTool(hash):
    file_hash = sanitize_hash(hash)
    if request.data == b'private':
        dbController.update_datapackage(query=f'Hash = "{file_hash}"', column_value={"Privacy": 1})
    return "Okay", 200


@app.route('/Marti/api/sync/metadata/<hash>/tool', methods=[const.GET])
@cross_origin(send_wildcard=True)
def getDataPackageTool(hash):
    file_hash = sanitize_hash(hash)
    file_list = os.listdir(os.path.join(Path(str(dp_directory)), Path(str(file_hash))))
    path = PurePath(dp_directory, str(file_hash), file_list[0])
    app.logger.info(f"Sending data package from {str(path)}")
    resp = send_file(str(path))
    return resp


@app.route('/Marti/sync/search', methods=[const.GET])
def retrieveData():
    logger.info('sync search triggered')
    keyword = request.args.get('keyword')
    packages = FlaskFunctions().getAllPackages()
    app.logger.info(f"Data packages in the database: {packages}")
    return str(packages)


@app.route('/Marti/sync/content', methods=const.HTTPMETHODS)
def specificPackage():
    from defusedxml import ElementTree as etree
    from os import listdir
    if request.method == 'GET' and request.args.get('uid') != None:
        data = request.data
        taskuid = request.args.get('uid')
        for file in listdir(config.ExCheckChecklistFilePath):
            try:
                xml = etree.parse(str(PurePath(Path(config.ExCheckChecklistFilePath), Path(file)))).getroot()
            except Exception as e:
                logger.error(e)
            tasks = xml.find('checklistTasks')
            for task in tasks:
                uid = task.find('uid')
                if str(uid.text) == str(taskuid):
                    return etree.tostring(task)
                else:
                    pass
        for file in listdir(config.ExCheckFilePath):
            try:
                xml = etree.parse(str(PurePath(Path(config.ExCheckFilePath), Path(file)))).getroot()
                if xml.find("checklistDetails").find('uid').text == str(taskuid):
                    return etree.tostring(xml)
            except Exception as e:
                logger.error(str(e))
    else:
        file_hash = sanitize_hash(request.args.get('hash'))

        if os.path.exists(str(PurePath(Path(dp_directory), Path(file_hash)))):
            logger.info('marti sync content triggerd')
            app.logger.debug(str(PurePath(Path(dp_directory), Path(file_hash))))
            file_list = os.listdir(str(PurePath(Path(dp_directory), Path(file_hash))))
            app.logger.debug(PurePath(Path(const.DATAPACKAGEFOLDER), Path(file_hash), Path(file_list[0])))
            path = PurePath(dp_directory, str(file_hash), file_list[0])
            app.logger.debug(str(path))
            return send_file(str(path))
        else:
            obj = dbController.query_ExCheck(verbose=True, query=f'hash = "{file_hash}"')
            data = etree.parse(str(PurePath(Path(config.ExCheckFilePath), Path(obj[0].data.filename))))
            data.getroot().find('checklistTasks').find("checklistTask").find("uid").text = data.getroot().find(
                'checklistTasks').find("checklistTask").find("checklistUid").text
            output = etree.tostring(data)
            return output


@app.route('/Marti/api/version', methods=[const.GET])
def returnVersion():
    logger.info('api version triggered')
    return const.versionInfo


@app.route('/Marti/sync/missionquery', methods=const.HTTPMETHODS)
def checkPresent():
    logger.info('synce missionquery triggered')
    file_hash = sanitize_hash(request.args.get('hash'))

    if FlaskFunctions().hashIsPresent(file_hash, dbController):
        app.logger.info(f"Data package with hash {file_hash} exists")
        if USINGSSL == False:
            return "http://" + IP + ':' + str(HTTPPORT) + "/Marti/api/sync/metadata/" + file_hash + "/tool"
        else:
            return "https://" + IP + ':' + str(HTTPPORT) + "/Marti/api/sync/metadata/" + file_hash + "/tool"
    else:
        app.logger.info(f"Data package with hash {file_hash} does not exist")
        return '404', 404


@app.route('/')
def home():
    return 'data package service is up, good job.'


# exCheck functions
"""   TODO End Points for 4.8 Support  
    The Execution Checklist (ExCheck) allows users to monitor and update the status of a shared 
    checklist that is hosted out on a TAK server. Each checklist is an instance of a template 
    that defines a number of tasks to be completed. 
   
    @app.route('/Marti/api/excheck/<checklistUid>/stop', methods=['POST'])
    @app.route('/Marti/api/excheck/<templateUid>/start', methods=['POST'])
    @app.route('/Marti/api/excheck/checklist', methods=['POST'])
    @app.route('/Marti/api/excheck/checklist/<checklistUid>', methods=['GET'])
    @app.route('/Marti/api/excheck/checklist/<checklistUid>/mission/<missionName>', methods=['PUT', 'DELETE'])
    @app.route('/Marti/api/excheck/checklist/<checklistUid>/status', methods=['GET', 'DELETE'])
    @app.route('/Marti/api/excheck/checklist/<checklistUid>/task/<taskUid>', methods=['GET', 'PUT','DELETE'])
    @app.route('/Marti/api/excheck/checklist/active', methods=['GET'])
    @app.route('/Marti/api/excheck/template', methods=['POST'])
    @app.route('/Marti/api/excheck/template/<templateUid>', methods=['GET', 'DELETE'])
    @app.route('/Marti/api/excheck/template/<templateUid>/task/<taskUid>', methods=['GET', 'PUT','DELETE','POST'])
"""


@app.route('/Marti/api/missions/exchecktemplates/changes', methods=['GET'])
def check_changes():
    try:
        # example return data {"version":"2","type":"MissionChange","data":[],"nodeId":"TAK-Server-a6htdf93"}
        # this endpoint should return any excheck template change since specified time
        # TODO: learn what squached represents
        request.args.get('squached')
        # the time since last connect and the length of time to check for changes
        request.args.get('start')
        return '{"version":"2","type":"MissionChange","data":[{"type":"REMOVE_CONTENT","missionName":"exchecktemplates","timestamp":"2020-10-23T16:44:10.346Z","creatorUid":"CN=testalpha,OU=Dev,O=FTS,L=Yarmouth,ST=NS,C=CA","serverTime":"2020-10-23T16:44:10.366Z","contentResource":{"filename":"d5d2bc15-f6ab-49e7-a408-5f7fe600ca3e.xml","keywords":["test bravo","this is in db","FEATHER"],"mimeType":"application/xml","name":"d5d2bc15-f6ab-49e7-a408-5f7fe600ca3e","submissionTime":"2020-10-20T00:18:57.157Z","submitter":"testbravo","uid":"d5d2bc15-f6ab-49e7-a408-5f7fe600ca3e","hash":"d94a49a958422a451b352b6ebd8b0741780214b1c2da4b0d41e6fca8e3674082","size":2155,"tool":"ExCheck"}},{"type":"REMOVE_CONTENT","missionName":"exchecktemplates","timestamp":"2020-10-23T16:44:10.235Z","creatorUid":"CN=testalpha,OU=Dev,O=FTS,L=Yarmouth,ST=NS,C=CA","serverTime":"2020-10-23T16:44:10.307Z","contentResource":{"hash":"f1197a7ec99442864b26fb58b993869303cd7ad4a7d6139611c0d42cd1ff156b"}},{"type":"REMOVE_CONTENT","missionName":"exchecktemplates","timestamp":"2020-10-23T16:44:10.186Z","creatorUid":"CN=testalpha,OU=Dev,O=FTS,L=Yarmouth,ST=NS,C=CA","serverTime":"2020-10-23T16:44:10.199Z","contentResource":{"filename":"4b730e6a-e2d8-48aa-9b9c-36dc09a0c462.xml","keywords":["ddd","wadasdsa","FEATHER"],"mimeType":"application/xml","name":"4b730e6a-e2d8-48aa-9b9c-36dc09a0c462","submissionTime":"2020-10-23T15:28:59.943Z","submitter":"testbravo","uid":"4b730e6a-e2d8-48aa-9b9c-36dc09a0c462","hash":"19597a47b4be14f9ee527630cf0dc7fb6b6de222502eab41b6c488e4371fb40b","size":1747,"tool":"ExCheck"}},{"type":"REMOVE_CONTENT","missionName":"exchecktemplates","timestamp":"2020-10-23T16:44:10.017Z","creatorUid":"CN=testalpha,OU=Dev,O=FTS,L=Yarmouth,ST=NS,C=CA","serverTime":"2020-10-23T16:44:10.127Z","contentResource":{"hash":"60aac7efcdf2d7001b8ad0d812e1d1528e252e01be130a6f6285b69943f8d633"}},{"type":"REMOVE_CONTENT","missionName":"exchecktemplates","timestamp":"2020-10-23T16:44:09.842Z","creatorUid":"CN=testalpha,OU=Dev,O=FTS,L=Yarmouth,ST=NS,C=CA","serverTime":"2020-10-23T16:44:09.875Z","contentResource":{"filename":"173992a0-d18d-46bb-b178-759011299d60.xml","keywords":["temp","temp 1","FEATHER"],"mimeType":"application/xml","name":"173992a0-d18d-46bb-b178-759011299d60","submissionTime":"2020-10-19T23:21:03.934Z","submitter":"testbravo","uid":"173992a0-d18d-46bb-b178-759011299d60","hash":"41482b4776bb7735654e8ddde2ad02032909b50ab4df5d8de55f99ebe6bc805d","size":1461,"tool":"ExCheck"}},{"type":"REMOVE_CONTENT","missionName":"exchecktemplates","timestamp":"2020-10-23T16:44:07.103Z","creatorUid":"CN=testalpha,OU=Dev,O=FTS,L=Yarmouth,ST=NS,C=CA","serverTime":"2020-10-23T16:44:07.138Z","contentResource":{"hash":"5bc1ac8bdbc28fc13ec002b60215a9c45874384e8fc754286c5d907a80219fc5"}},{"type":"ADD_CONTENT","missionName":"exchecktemplates","timestamp":"2020-10-23T15:28:59.947Z","creatorUid":"S-1-5-21-2720623347-3037847324-4167270909-1002","serverTime":"2020-10-23T15:28:59.963Z","contentResource":{"filename":"4b730e6a-e2d8-48aa-9b9c-36dc09a0c462.xml","keywords":["ddd","wadasdsa","FEATHER"],"mimeType":"application/xml","name":"4b730e6a-e2d8-48aa-9b9c-36dc09a0c462","submissionTime":"2020-10-23T15:28:59.943Z","submitter":"testbravo","uid":"4b730e6a-e2d8-48aa-9b9c-36dc09a0c462","hash":"19597a47b4be14f9ee527630cf0dc7fb6b6de222502eab41b6c488e4371fb40b","size":1747,"tool":"ExCheck"}},{"type":"ADD_CONTENT","missionName":"exchecktemplates","timestamp":"2020-10-23T15:26:45.110Z","creatorUid":"S-1-5-21-2720623347-3037847324-4167270909-1002","serverTime":"2020-10-23T15:26:45.116Z"}],"nodeId":"TAK-Server-560c34e9"}'
    except Exception as e:
        print('exception in check changes' + str(e))

# TODO remove?
@app.route('/Marti/api/missions/exchecktemplates/subscription', methods=['PUT'])
def request_subscription():
    try:
        # this endpoint allows for the client to request a new subscription
        # possibly the uid of the client db also contains create_time and mission_id
        print(request.args.get('uid'))

        return ('', 200)
    except Exception as e:
        print('exception in request_subscription' + str(e))

@app.route('/Marti/api/missions/exchecktemplates', methods=['GET'])
def exchecktemplates():
    return ExCheckController().exchecktemplates()

@app.route('/Marti/api/missions/ExCheckTemplates', methods=['GET'])
def ExCheckTemplates():
    return ExCheckController().exchecktemplates()

@app.route('/Marti/api/missions/<templateuid>/subscription', methods=['DELETE', 'PUT'])
def missionupdate(templateuid):
    from flask import request
    uid = request.args.get('uid')
    return '', 200

@app.route('/Marti/api/excheck/template', methods=['POST'])
def template():
    return ExCheckController().template(PIPE)

@app.route('/Marti/api/excheck/<subscription>/start', methods=['POST'])
def startList(subscription):
    return ExCheckController().startList(subscription)

@app.route('/Marti/api/excheck/checklist/', methods=["POST"])
def update_checklist():
    return ExCheckController().update_checklist()

@app.route('/Marti/api/excheck/checklist/<checklistid>')
def accesschecklist(checklistid):
    return ExCheckController().accesschecklist(checklistid)

@app.route('/Marti/api/excheck/checklist/<checklistid>/task/<taskid>', methods=['PUT'])
def updatetemplate(checklistid, taskid):
    return ExCheckController().updatetemplate(checklistid, taskid, PIPE)

# TODO remove ?
@app.route('/Marti/sync/content')
def sync():
    # this endpoint was triggered on attempting to create new template from existing template
    # likely the hash of the excheck
    y = request
    request.args.get('hash')
    uid = request.args.get('uid')
    return '', 200

@app.route('/Marti/api/excheck/checklist/active', methods=["GET"])
def activechecklists():
    return ExCheckController().activechecklists()

# TODO remove?
def sanitize_path_input(user_input: str) -> bool:
    """ this function takes a file hash and validates it's
    content to avoid RCE and XSS attacks

    Args:
        user_input: any user input which is used to write a path
    """
    return True
    # temporarily removed as it broke some tak clients
    #if re.match("^[A-Za-z0-9_-]*$", user_input):
    #    return True
    #else:
    #    return False

def sanitize_hash(hash: str) -> str:
    return escape(hash)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class FlaskFunctions:

    def __init__(self):
        self.callsigns = []

    def create_dp(self, dbController, **args):
        return dbController.create_datapackage(**args)

    def hashIsPresent(self, hash, dbControl):
        data = dbControl.query_datapackage(query=f'Hash = "{hash}"')
        return len(data) > 0

    def getSubmissionUser(self, UID, dbControl):
        callsign = dbControl.query_user(query=f'uid = "{UID}"', column=['callsign'])
        return callsign

    def getAllPackages(self):
        data = DatabaseController().query_datapackage("Privacy = 0")
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

    def startup(self, ip, port, pipe):
        try:
            from eventlet import wsgi


            init_config()
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
            # app.run(host='0.0.0.0', port=8080)
            wsgi.server(eventlet.listen((DataPackageServerConstants().IP, int(HTTPPORT))), app)

        except Exception as e:
            logger.error('there has been an exception in Data Package service startup ' + str(e))
            return -1

    def stop(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def setIP(self, IP_to_be_set):
        global IP
        IP = IP_to_be_set

    def getIP(self):
        global IP
        return IP

    def setHTTPPORT(self, HTTPPORTToBeSet):
        global HTTPPORT
        HTTPPORT = HTTPPORTToBeSet

    def getHTTPPort(self):
        global HTTPPORT
        return HTTPPORT

    def setPIPE(self, PIPEtoBeSet):
        global PIPE
        PIPE = PIPEtoBeSet

    def getPIPE(self):
        global PIPE
        return PIPE

    def setSSL(self, SSL: bool):
        global USINGSSL
        USINGSSL = SSL

    def getSSL(self):
        global USINGSSL
        return USINGSSL
