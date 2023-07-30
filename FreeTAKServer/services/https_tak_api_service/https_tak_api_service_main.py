"""this module is responsible for running the DataPackage service
as it utilizes flask, each method represents an endpoint
this web server is responsible for all HTTP queries to
FTS from an ATAK client"""
import logging
import os
import random
import string
import traceback
from typing import Dict
import defusedxml.ElementTree as ET
from logging.handlers import RotatingFileHandler
from pathlib import Path, PurePath

from digitalpy.core.service_management.digitalpy_service import DigitalPyService
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.response import Response
from digitalpy.core.parsing.formatter import Formatter

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
from flask import Flask, request, send_file, escape, make_response
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
"""
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
"""
"""
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
"""

@app.route('/Marti/sync/search', methods=[const.GET])
def retrieveData():
    logger.info('sync search triggered')
    keyword = request.args.get('keyword')
    packages = FlaskFunctions().getAllPackages()
    app.logger.info(f"Data packages in the database: {packages}")
    return str(packages)

@app.route('/Marti/api/version', methods=[const.GET])
def returnVersion():
    logger.info('api version triggered')
    return const.versionInfo

"""
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
"""

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

@app.route('/Marti/api/excheck/template/<templateUid>/task/<taskUid>', methods=['GET', 'PUT','DELETE','POST'])
def excheck_template_task(templateUid, taskUid):
    if request.method == "GET":
        return ExCheckController().get_excheck_template_task(templateUid, taskUid, request.data)
    elif request.method == "POST":
        return ExCheckController().create_excheck_template_task(templateUid, taskUid, request.data)

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

"""
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
"""
""" 
@app.route('/Marti/api/missions/<templateuid>/subscription', methods=['DELETE', 'PUT'])
def missionupdate(templateuid):
    from flask import request
    uid = request.args.get('uid')
    return '', 200
"""
"""
@app.route('/Marti/sync/content', methods=const.HTTPMETHODS)
def specificPackage():
    from defusedxml import ElementTree as etree
    from os import listdir
    try:
        if request.method == 'GET' and request.args.get('uid') != None:
            dp_request = ObjectFactory.get_instance("request")
            dp_response = ObjectFactory.get_instance("response")
            enterprisesync_facade = ObjectFactory.get_instance("EnterpriseSync")
            enterprisesync_facade.initialize(dp_request, dp_response)
            enterprisesync_facade.get_enterprise_sync_data(objectuid = request.args.get('uid'))
            return dp_response.get_value("objectdata"), 200
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
                dp_request = ObjectFactory.get_instance("request")
                dp_response = ObjectFactory.get_instance("response")
                enterprisesync_facade = ObjectFactory.get_instance("EnterpriseSync")
                enterprisesync_facade.initialize(dp_request, dp_response)
                enterprisesync_facade.get_enterprise_sync_data(objecthash = request.args.get('hash'))
                return dp_response.get_value("objectdata"), 200
    except Exception as ex:
        print(ex)
        return '', 500
"""

@app.route('/Marti/api/excheck/checklist/', methods=["POST"])
def update_checklist():
    return ExCheckController().update_checklist()

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

APPLICATION_PROTOCOL = "xml"
API_REQUEST_TIMEOUT = 5000

from eventlet import listen, wrap_ssl, wsgi
import ssl
import time

from FreeTAKServer.model.sockets.SSLServerSocket import SSLServerSocket
from FreeTAKServer.core.connection.SSLSocketController import SSLSocketController

from .blueprints import excheck_blueprint, citrap_blueprint, misc_blueprint, mission_blueprint, enterprise_sync_blueprint

class HTTPSTakAPI(DigitalPyService):
     # a dictionary containing the request_id and response objects for all received requests
    # to prevent confusion between endpoints
    responses: Dict[str, Response] = {}

    def __init__(self, service_id: str, subject_address: str, subject_port: int, subject_protocol, integration_manager_address: str, integration_manager_port: int, integration_manager_protocol: str, formatter: Formatter):
        super().__init__(service_id, subject_address, subject_port, subject_protocol, integration_manager_address, integration_manager_port, integration_manager_protocol, formatter)

    def get_response_in_responses(self, id):
        # check if the response has already been received
        if self.responses.get(id) != None:
            # pop item so dictionary doesn't fill up
            response = self.responses.pop(id)
            return response
        
    def retrieve_response(self, id: str):
        """wait to retrieve a response from the broker this is mainly
        to prevent cases where multiple requests are being processed 
        simultaneously causing a possible mismatch of responses between
        requests, instead we pass the id to this method which then checks
        in the responses dict if the response has been received by another
        thread, if not then it goes on receiving the next response
        Args:
            id (str): the id of the response being waited for
        """
        # check if the response has already been received
        existing_response = self.get_response_in_responses(id)
        if existing_response is not None:
            return existing_response

        start_time = time.time()

        # Start the loop
        while (time.time() - start_time) < API_REQUEST_TIMEOUT:
            # the poller is only registered to the zmq_subscriber socket
            # so if there are available messages it should only be coming
            # from the zmq_subscriber socket.
            self.subscriber_socket.RCVTIMEO = 1000

            responses = super().broker_receive(blocking=True)
            for response in responses:
                if response.get_id() != id:
                    # use shared memory of responses dictionary
                    self.responses[response.get_id()] = response
                else:
                    return response
                    
                # check if the response has already been received
                existing_response = self.get_response_in_responses(id)
                if existing_response is not None:
                    return existing_response

        # check if the response has already been received
        existing_response = self.get_response_in_responses(id)
        if existing_response is not None:
            return existing_response
        else:
            raise TimeoutError("zmanager failed to return a response")

    def start(self, ip, port, factory):
        try:
            global IP, HTTPPORT
            init_config()
            self.MainSocket = SSLServerSocket()
            IP = ip
            HTTPPORT = port
            self.initialize_connections(APPLICATION_PROTOCOL)
            ObjectFactory.configure(factory)
            # Make sure the data package directory exists
            # Create the relevant database tables
            print(const.IP)
            print(HTTPPORT)
            self.setIP(IP)
            self.setHTTPPORT(HTTPPORT)
            #wsgi.server(eventlet.listen(('', 14533)), app)  keyfile=config.keyDir,
            self.SSLSocketController = SSLSocketController()
            self.SSLSocketController.changeIP(IP)
            self.SSLSocketController.changePort(HTTPPORT)
            self.setSSL(True)
            self.register_blueprints(app)
            wsgi.server(sock=wrap_ssl(listen((DataPackageServerConstants().IP, int(HTTPPORT))), keyfile=config.unencryptedKey,
                                      certfile=config.pemDir,
                                      server_side=True, ca_certs=config.CA, cert_reqs=ssl.CERT_REQUIRED), site=app)
        except Exception as e:
            logger.error('there has been an exception in Data Package service startup ' + str(e))
            return -1


    def register_blueprints(self, app):
        app.register_blueprint(excheck_blueprint.page)
        app.register_blueprint(citrap_blueprint.page)
        app.register_blueprint(misc_blueprint.page)
        app.register_blueprint(mission_blueprint.page)
        app.register_blueprint(enterprise_sync_blueprint.page)
        
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

    def setSSL(self, SSL: bool):
        global USINGSSL
        USINGSSL = SSL

    def getSSL(self):
        global USINGSSL
        return USINGSSL

    def stop(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

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
