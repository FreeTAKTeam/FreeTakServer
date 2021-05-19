import logging
import os
import random
import string
import traceback
import defusedxml.ElementTree as ET
from logging.handlers import RotatingFileHandler
from pathlib import Path, PurePath
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.controllers.configuration.SQLcommands import SQLcommands
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.controllers.configuration.DatabaseConfiguration import DatabaseConfiguration
import eventlet
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from flask_cors import CORS, cross_origin

loggingConstants = LoggingConstants()
logger = CreateLoggerController("DataPackageServer").getLogger()
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, send_file
from flask.logging import default_handler

dbController = DatabaseController()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

USINGSSL = False

sql = SQLcommands()
const = DataPackageServerConstants()
log = LoggingConstants()

app = Flask(__name__)  # create the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConfiguration().DataBaseConnectionString
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'vnkdjnfjknfl1232#'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
# TODO: verify session life cycle in dbController doesnt break this logic
dbController.session = db.session
file_dir = os.path.dirname(os.path.realpath(__file__))
dp_directory = MainConfig.DataPackageFilePath

if not os.path.exists(MainConfig.ExCheckMainPath):
    os.mkdir(MainConfig.ExCheckMainPath)

if not os.path.exists(MainConfig.ExCheckChecklistFilePath):
    os.mkdir(MainConfig.ExCheckChecklistFilePath)

if not os.path.exists(MainConfig.ExCheckFilePath):
    os.mkdir(MainConfig.ExCheckFilePath)
# Set up logging
"""if not Path(log.LOGDIRECTORY).exists():
    print(f"Creating directory at {log.LOGDIRECTORY}")
    os.makedirs(log.LOGDIRECTORY)"""
app.logger.removeHandler(default_handler)
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
            streams = dbController.query_videostream(query=f'uid = "{uid}"')
            if len(streams) > 0:
                app.logger.info(f"Already received feed with UID={uid} (alias = {alias})")
                continue  # Ignore this feed if there are duplicates
            app.logger.info(f"Inserting video feed into database: {request.data.decode('utf-8')}")
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
    logger.info('dataoackage upload started')
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
    if request.data == b'private':
        dbController.update_datapackage(query=f'Hash = "{hash}"', column_value={"Privacy": 1})
    return "Okay", 200


@app.route('/Marti/api/sync/metadata/<hash>/tool', methods=[const.GET])
@cross_origin(send_wildcard = True)
def getDataPackageTool(hash):
    from flask import make_response
    file_list = os.listdir(str(dp_directory) + '/' + str(hash))
    path = PurePath(dp_directory, str(hash), file_list[0])
    app.logger.info(f"Sending data package from {str(path)}")
    resp = send_file(str(path))
    return resp


@app.route('/Marti/sync/search', methods=[const.GET])
def retrieveData():
    logger.info('sync search tirggerd')
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
        for file in listdir(MainConfig.ExCheckChecklistFilePath):
            xml = etree.parse(str(PurePath(Path(MainConfig.ExCheckChecklistFilePath), Path(file)))).getroot()

            tasks = xml.find('checklistTasks')
            for task in tasks:
                uid = task.find('uid')
                if str(uid.text) == str(taskuid):
                    return etree.tostring(task)
                else:
                    pass
        for file in listdir(MainConfig.ExCheckFilePath):
            xml = etree.parse(str(PurePath(Path(MainConfig.ExCheckFilePath), Path(file)))).getroot()
            if xml.find("checklistDetails").find('uid').text == str(taskuid):
                return etree.tostring(xml)

    else:
        hash = request.args.get('hash')
        import hashlib
        if os.path.exists(str(PurePath(Path(dp_directory), Path(hash)))):
            logger.info('marti sync content triggerd')
            app.logger.debug(str(PurePath(Path(dp_directory), Path(hash))))
            file_list = os.listdir(str(PurePath(Path(dp_directory), Path(hash))))
            app.logger.debug(PurePath(Path(const.DATAPACKAGEFOLDER), Path(hash), Path(file_list[0])))
            path = PurePath(dp_directory, str(hash), file_list[0])
            app.logger.debug(str(path))
            return send_file(str(path))
        else:
            obj = dbController.query_ExCheck(verbose=True, query=f'hash = "{hash}"')
            data = etree.parse(str(PurePath(Path(MainConfig.ExCheckFilePath), Path(obj[0].data.filename))))
            data.getroot().find('checklistTasks').find("checklistTask").find("uid").text = data.getroot().find('checklistTasks').find("checklistTask").find("checklistUid").text
            output = etree.tostring(data, pretty_print=False)
            return output


@app.route('/Marti/api/version', methods=[const.GET])
def returnVersion():
    logger.info('api version triggered')
    return const.versionInfo


@app.route('/Marti/sync/missionquery', methods=const.HTTPMETHODS)
def checkPresent():
    logger.info('synce missionquery triggered')
    hash = request.args.get('hash')
    if FlaskFunctions().hashIsPresent(hash, dbController):
        app.logger.info(f"Data package with hash {hash} exists")
        if USINGSSL == False:
            return "http://" + IP + ':' + str(HTTPPORT) + "/Marti/api/sync/metadata/" + hash + "/tool"
        else:
            return "https://" + IP + ':' + str(HTTPPORT) + "/Marti/api/sync/metadata/" + hash + "/tool"
    else:
        app.logger.info(f"Data package with hash {hash} does not exist")
        return '404', 404


@app.route('/')
def home():
    return 'data package service is up, good job.'



#exCheckStuff
from flask import Flask, request
from FreeTAKServer.controllers.ExCheckControllers.templateToJsonSerializer import templateSerializer
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

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
    try:
        # when no data available
        # return b'{"version":"2","type":"Mission","data":[{"name":"exchecktemplates","description":"","chatRoom":"","tool":"ExCheck","keywords":[],"creatorUid":"ExCheck","createTime":"2020-10-19T22:37:39.290Z","externalData":[],"uids":[],"contents":[]}],"nodeId":"TAK-Server-560c34e9"}'
        # when data available
        return templateSerializer().convert_object_to_json(DatabaseController().query_ExCheck())
    except Exception as e:
        print(e)
@app.route('/Marti/api/missions/ExCheckTemplates', methods=['GET'])
def ExCheckTemplates():
    try:
        # when no data available
        # return b'{"version":"2","type":"Mission","data":[{"name":"exchecktemplates","description":"","chatRoom":"","tool":"ExCheck","keywords":[],"creatorUid":"ExCheck","createTime":"2020-10-19T22:37:39.290Z","externalData":[],"uids":[],"contents":[]}],"nodeId":"TAK-Server-560c34e9"}'
        # when data available
        return templateSerializer().convert_object_to_json(DatabaseController().query_ExCheck())
    except Exception as e:
        print(e)

@app.route('/Marti/api/missions/<templateuid>/subscription', methods=['DELETE', 'PUT'])
def missionupdate(templateuid):
    from flask import request
    uid = request.args.get('uid')
    return '', 200

@app.route('/Marti/api/excheck/template', methods=['POST'])
def template():
    try:
        import uuid
        xmlstring = f'<?xml version="1.0"?><event version="2.0" uid="{uuid.uuid4()}" type="t-x-m-c" time="2020-11-28T17:45:51.000Z" start="2020-11-28T17:45:51.000Z" stale="2020-11-28T17:46:11.000Z" how="h-g-i-g-o"><point lat="0.00000000" lon="0.00000000" hae="0.00000000" ce="9999999" le="9999999" /><detail><mission type="CHANGE" tool="ExCheck" name="exchecktemplates" authorUid="S-1-5-21-2720623347-3037847324-4167270909-1002"><MissionChanges><MissionChange><contentResource><filename>61b01475-ad44-4300-addc-a9474ebf67b0.xml</filename><hash>018cd5786bd6c2e603beef30d6a59987b72944a60de9e11562297c35ebdb7fd6</hash><keywords>test init</keywords><keywords>dessc init</keywords><keywords>FEATHER</keywords><mimeType>application/xml</mimeType><name>61b01475-ad44-4300-addc-a9474ebf67b0</name><size>1522</size><submissionTime>2020-11-28T17:45:47.980Z</submissionTime><submitter>wintak</submitter><tool>ExCheck</tool><uid>61b01475-ad44-4300-addc-a9474ebf67b0</uid></contentResource><creatorUid>S-1-5-21-2720623347-3037847324-4167270909-1002</creatorUid><missionName>exchecktemplates</missionName><timestamp>2020-11-28T17:45:47.983Z</timestamp><type>ADD_CONTENT</type></MissionChange></MissionChanges></mission></detail></event>'
        # this is where the client will post the xmi of a template
        from flask import request
        from datetime import datetime
        from defusedxml import ElementTree as etree
        import hashlib
        # possibly the uid of the client submitting the template
        Y = request
        uid = request.args.get('clientUid')
        XMI = request.data.decode()
        serializer = templateSerializer(XMI)
        object = serializer.convert_template_to_object()
        object.timestamp = datetime.strptime(object.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        serializer.create_DB_object(object)
        xml = etree.fromstring(XMI)
        tasks = xml.find('checklistTasks')
        path = str(PurePath(Path(MainConfig.ExCheckFilePath), Path(f'{object.data.uid}.xml')))
        with open(path, 'w+') as file:
            file.write(XMI)
            file.close()

        uid = object.data.uid
        temp = etree.fromstring(XMI)
        cot = etree.fromstring(xmlstring)
        resources = cot.find('detail').find('mission').find('MissionChanges').find('MissionChange').find('contentResource')
        resources.find('filename').text = temp.find('checklistDetails').find('uid').text + '.xml'
        resources.findall('keywords')[0].text = temp.find('checklistDetails').find('name').text
        resources.findall('keywords')[1].text = temp.find('checklistDetails').find('description').text
        resources.findall('keywords')[2].text = temp.find('checklistDetails').find('creatorCallsign').text
        resources.find('uid').text = temp.find('checklistDetails').find('uid').text
        resources.find('name').text = temp.find('checklistDetails').find('uid').text
        resources.find('size').text = str(len(XMI))
        resources.find('hash').text = str(hashlib.sha256(str(XMI).encode()).hexdigest())
        z = etree.tostring(cot)
        from FreeTAKServer.model.testobj import testobj
        object = testobj()
        object.xmlString = z
        PIPE.put(object)
        return str(uid), 200
    except Exception as e:
        print(str(e))

@app.route('/Marti/api/excheck/<subscription>/start', methods=['POST'])
def startList(subscription):
    import uuid
    from defusedxml import ElementTree as etree
    from lxml.etree import Element
    import datetime
    uid = str(uuid.uuid4())
    r = request
    # client uid
    request.args.get('clientUid')
    # name of template
    request.args.get('name')
    # description of template
    request.args.get('description')
    # startTime of template
    startTime = request.args.get('startTime')
    # callsign of submission user
    request.args.get('callsign')

    with open(str(PurePath(Path(MainConfig.ExCheckChecklistFilePath), Path(f'{uid}.xml'))), 'w+') as file:
        file.write(str(open(str(PurePath(Path(MainConfig.ExCheckFilePath), Path(f'{subscription}.xml'))), 'r').read()))
        file.close()

    xml = etree.parse(
        MainConfig.ExCheckChecklistFilePath + '/' + uid + '.xml').getroot()

    starttime = Element('startTime')
    starttime.text = startTime
    details = xml.find('checklistDetails')
    if details.find('startTime') == None:

        details.append(starttime)
    else:
        details.find('startTime').text = startTime
    uids = details.find('uid')
    uids.text = uid
    details.find('description').text = request.args.get('description')
    details.find('name').text = request.args.get('name')

    tasks = xml.find('checklistTasks')
    for task in tasks:
        taskuid = task.find('uid')
        taskuid.text = str(uuid.uuid4())


    with open(
            str(PurePath(Path(MainConfig.ExCheckChecklistFilePath), Path(uid + '.xml'))),
            'w+') as file:
        y = etree.tostring(xml)
        file.write(etree.tostring(xml).decode())
        file.close()

    excheckobj = dbController.query_ExCheck(f'ExCheckData.uid = "{subscription}"', verbose=True,)[0]
    dbController.create_Excheckchecklist(startTime=datetime.datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S.%fZ'), creatorUid = request.args.get('clientUid'), description = request.args.get('description'), callsign = request.args.get('callsign'), name = request.args.get('name'), uid = uid, filename = f'{uid}.xml', template = excheckobj)

    return str(open(str(PurePath(Path(MainConfig.ExCheckChecklistFilePath), Path(uid + '.xml'))), 'r').read()), 200

@app.route('/Marti/api/excheck/checklist/<checklistid>')
def accesschecklist(checklistid):
    return str(open(str(PurePath(Path(MainConfig.ExCheckChecklistFilePath), Path(checklistid + '.xml'))),
              'r').read())

@app.route('/Marti/api/excheck/checklist/<checklistid>/task/<taskid>', methods=['PUT'])
def updatetemplate(checklistid, taskid):
    from flask import request
    from defusedxml import ElementTree as etree
    from FreeTAKServer.controllers.SpecificCoTControllers.SendExcheckUpdateController import SendExcheckUpdateController
    from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
    from FreeTAKServer.model.FTSModel.Event import Event
    from FreeTAKServer.model.RawCoT import RawCoT
    import uuid
    import hashlib


    data = request.data

    xml = etree.parse(
        str(PurePath(Path(MainConfig.ExCheckChecklistFilePath), Path(checklistid + '.xml')))).getroot()
    updatedTask = etree.fromstring(data)
    tasks = xml.find('checklistTasks')
    for task in tasks:
        uid = task.find('uid')
        if uid.text == taskid:
            tasks.replace(task, updatedTask)
        else:
            pass
    with open(
            str(PurePath(Path(MainConfig.ExCheckChecklistFilePath), Path(checklistid + '.xml'))), 'w+') as file:
        file.write(etree.tostring(xml).decode())
        file.close()

    # Create Object to send to client
    object = Event.ExcheckUpdate()
    object.setuid(str(uuid.uuid4()))
    object.setversion('2.0')
    object.detail.mission.settype("CHANGE")
    object.detail.mission.settool("ExCheck")
    object.detail.mission.setname(checklistid)
    object.detail.mission.setauthorUid(request.args.get("clientUid"))
    object.detail.mission.MissionChanges.MissionChange.creatorUid.setINTAG(request.args.get("clientUid"))
    object.detail.mission.MissionChanges.MissionChange.missionName.setINTAG(checklistid)
    object.detail.mission.MissionChanges.MissionChange.type.setINTAG("ADD_CONTENT")
    object.detail.mission.MissionChanges.MissionChange.contentResource.filename.setINTAG(taskid+'.xml')
    object.detail.mission.MissionChanges.MissionChange.contentResource.hash.setINTAG(str(hashlib.sha256(str(open(MainConfig.ExCheckChecklistFilePath + '/' + checklistid + '.xml', 'r')).encode()).hexdigest()))
    object.detail.mission.MissionChanges.MissionChange.contentResource.keywords.setINTAG('Task')
    object.detail.mission.MissionChanges.MissionChange.contentResource.name.setINTAG(taskid)
    object.detail.mission.MissionChanges.MissionChange.contentResource.size.setINTAG(str(len(data)))
    #TODO: change this value
    object.detail.mission.MissionChanges.MissionChange.contentResource.submitter.setINTAG('atak')
    object.detail.mission.MissionChanges.MissionChange.contentResource.uid.setINTAG(taskid)



    '''object = etree.fromstring(templateex)
    object.uid = uuid.uuid4()
    object.find('detail').find('mission').type= "CHANGE"
    object.find('detail').find('mission').name = taskid
    object.find('detail').find('mission').Uid = request.args.get("clientUid")
    object.find('detail').find('mission').find('MissionChanges').find('MissionChange').find('creatorUid').text = request.args.get("clientUid")
    object.find('detail').find('mission').find('MissionChanges').find('MissionChange').find('missionName').text = taskid
    object.find('detail').find('mission').find('MissionChanges').find('MissionChange').find('filename').text = checklistid+'.xml'
    object.detail.mission.MissionChanges.MissionChange.contentResource.hash.setINTAG(str(hashlib.sha256(str(data).encode()).hexdigest()))
    object.detail.mission.MissionChanges.MissionChange.contentResource.keywords.setINTAG('Task')
    object.detail.mission.MissionChanges.MissionChange.contentResource.name.setINTAG(checklistid)
    object.detail.mission.MissionChanges.MissionChange.contentResource.size.setINTAG(str(len(data)))
    #TODO: change this value
    object.detail.mission.MissionChanges.MissionChange.contentResource.submitter.setINTAG('test')
    object.detail.mission.MissionChanges.MissionChange.contentResource.uid.setINTAG(checklistid)'''
    rawcot = RawCoT()
    xml = XMLCoTController().serialize_model_to_CoT(object)
    rawcot.xmlString = xml

    PIPE.put(rawcot)
    #PIPE.send()

    return '', 200

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
    from os import listdir
    from FreeTAKServer.model.FTSModel.Checklists import Checklists
    from FreeTAKServer.model.FTSModel.Checklist import Checklist
    from lxml.etree import Element
    from defusedxml import ElementTree as etree
    checklists = Checklists.Checklist()
    rootxml = Element('checklists')

    for file in listdir(MainConfig.ExCheckChecklistFilePath):
        checklist = Element('checklist')
        xmldetails = etree.parse(str(PurePath(Path(MainConfig.ExCheckChecklistFilePath), Path(file)))).getroot().find('checklistDetails')
        checklist.append(xmldetails)
        checklist.append(Element('checklistColumns'))
        checklist.append(Element('checklistTasks'))
        rootxml.append(checklist)

    xml = etree.tostring(rootxml)
    return xml
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

if __name__ == "__main__":
    pass
