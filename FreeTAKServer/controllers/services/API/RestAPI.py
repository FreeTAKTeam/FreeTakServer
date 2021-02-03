from pathlib import PurePath, Path
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_httpauth import HTTPTokenAuth
from flask_login import LoginManager
import threading
import string
import hashlib
from zipfile import ZipFile
from lxml import etree
import uuid
from FreeTAKServer.model.SQLAlchemy.User import User
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.RawCoT import RawCoT
from FreeTAKServer.controllers.ApplyFullJsonController import ApplyFullJsonController
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.model.ServiceObjects.FTS import FTS
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables as vars
from FreeTAKServer.model.SimpleClient import SimpleClient
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.controllers.configuration.DatabaseConfiguration import DatabaseConfiguration
from FreeTAKServer.controllers.RestMessageControllers.SendChatController import SendChatController
import os
import shutil
import json
from flask_cors import CORS
from FreeTAKServer.controllers.RestMessageControllers.SendSimpleCoTController import SendSimpleCoTController
from FreeTAKServer.controllers.RestMessageControllers.SendPresenceController import SendPresenceController
from FreeTAKServer.controllers.RestMessageControllers.SendEmergencyController import SendEmergencyController
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from FreeTAKServer.controllers.JsonController import JsonController

dbController = DatabaseController()

UpdateArray = []
StartTime = None

functionNames = vars()
functionNames.function_names()

jsonVars = vars()
jsonVars.json_vars()

restMethods = vars()
restMethods.rest_methods()

defaultValues = vars()
defaultValues.default_values()

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
auth = HTTPTokenAuth(scheme='Bearer')
app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConfiguration().DataBaseConnectionString
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
dbController.session = db.session
CORS(app)
socketio = SocketIO(app, async_handlers=True, async_mode="eventlet")
socketio.init_app(app, cors_allowed_origins="*")
APIPipe = None
CommandPipe = None
app.config["SECRET_KEY"] = 'vnkdjnfjknfl1232#'


@app.errorhandler(404)
def page_not_found(e):
    return 'this endpoint does not exist'


@auth.verify_token
def verify_token(token):
    if token:
        output = dbController.query_APIUser(query=f'token == "{token}"')
        if output:
            return output[0].Username
        else:
            output = dbController.query_systemUser(query=f'token == "{token}"')
            if output:
                return output[0].name


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


def socket_auth(session=None):
    def innerfunc(x):
        def wrapper(*args, **kwargs):
            if hasattr(session, 'authenticated') and session.authenticated:
                x(*args, **kwargs)
            else:
                pass

        return wrapper

    return innerfunc


@app.route('/Alive')
def sessions():
    return b'API is running', 200


@socketio.on('connect')
def connection():
    emit('connectUpdate', json.dumps({"starttime": str(StartTime), "version": str(MainConfig.version)}))


@socketio.on('authenticate')
def authenticate(token):
    if json.loads(token)["Authenticate"] == "a@v{5]MQU><waQ;Z":
        emit('authentication', json.dumps({'successful': 'True'}))
        session.authenticated = True
    else:
        emit('authentication', json.dumps({'successful': 'False'}))


@socketio.on('users')
@socket_auth(session=session)
def show_users(empty=None):
    output = dbController.query_user()
    for i in range(0, len(output)):
        try:
            original = output[i]
            output[i] = output[i].__dict__
            print(output[i])
            try:
                output[i]['callsign'] = original.CoT.detail.contact.callsign
                output[i]['team'] = original.CoT.detail._group.name
            except BaseException:
                output[i]['callsign'] = "undefined"
                output[i]['team'] = "undefined"
            del (output[i]['_sa_instance_state'])
            del (output[i]['CoT_id'])
            del (output[i]['CoT'])
        except Exception as e:
            print(e)
    socketio.emit('userUpdate', json.dumps({"Users": output}))


@socketio.on('logs')
@socket_auth(session=session)
def return_logs(time):
    from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
    import datetime
    log_data = {'log_data': []}
    for line in reversed(open(LoggingConstants().ERRORLOG, "r").readlines()):
        timeoflog = line.split(" : ")[1]
        if datetime.datetime.strptime(timeoflog, '%Y-%m-%d %H:%M:%S,%f') > datetime.datetime.strptime(
                json.loads(time)["time"], '%Y-%m-%d %H:%M:%S,%f'):
            outline = {"time": '', "type": '', 'file': '', 'message': ''}
            line_segments = line.split(" : ")
            outline["type"] = line_segments[0]
            outline["time"] = line_segments[1]
            outline["file"] = line_segments[2]
            outline["message"] = line_segments[3]
            log_data['log_data'].append(outline)
        else:
            break
    emit("logUpdate", json.dumps(log_data))


@socketio.on('serviceInfo')
@socket_auth(session=session)
def show_service_info(empty=None):
    mapping = {"start": "on", "stop": "off", "": ""}
    FTSServerStatusObject = getStatus()
    tcpcot = FTSServerStatusObject.CoTService
    sslcot = FTSServerStatusObject.SSLCoTService
    restapi = FTSServerStatusObject.RestAPIService
    tcpdp = FTSServerStatusObject.TCPDataPackageService
    ssldp = FTSServerStatusObject.SSLDataPackageService
    fedserver = FTSServerStatusObject.FederationServerService
    jsonObject = {"services":
                  {"TCP_CoT_service": {"status": mapping[tcpcot.CoTServiceStatus], "port": tcpcot.CoTServicePort},
                   "SSL_CoT_service": {"status": mapping[sslcot.SSLCoTServiceStatus],
                                       "port": sslcot.SSLCoTServicePort},
                   "TCP_DataPackage_service": {"status": mapping[tcpdp.TCPDataPackageServiceStatus],
                                               "port": tcpdp.TCPDataPackageServicePort},
                   "SSL_DataPackage_service": {"status": mapping[ssldp.SSLDataPackageServiceStatus],
                                               "port": ssldp.SSLDataPackageServicePort},
                   "Federation_server_service": {"status": mapping[fedserver.FederationServerServiceStatus],
                                                 "port": fedserver.FederationServerServicePort},
                   "Rest_API_service": {"status": mapping[restapi.RestAPIServiceStatus],
                                        "port": restapi.RestAPIServicePort}},
                  "ip": tcpdp.TCPDataPackageServiceIP
                  }
    emit('serviceInfoUpdate', json.dumps(jsonObject))


def getStatus():
    CommandPipe.send([functionNames.checkStatus])
    return CommandPipe.recv()


@socketio.on("serverHealth")
@socket_auth(session=session)
def serverHealth(empty=None):
    import psutil
    import pathlib
    import os
    jsondata = {
        "CPU": int(psutil.cpu_percent(interval=0.1)),
        "memory": int(psutil.virtual_memory().percent),
        "disk": int(psutil.disk_usage(str(pathlib.Path(os.getcwd()).anchor)).percent)
    }
    emit('serverHealthUpdate', json.dumps(jsondata))


@socketio.on('systemStatus')
@socket_auth(session=session)
def systemStatus(update=None):
    print('system status running')
    from FreeTAKServer.controllers.ServerStatusController import ServerStatusController
    currentStatus = getStatus()
    statusObject = ServerStatusController(currentStatus)
    jsondata = ApplyFullJsonController().serialize_model_to_json(statusObject)
    emit('systemStatusUpdate', json.dumps(jsondata))


@socketio.on('changeServiceInfo')
# @socket_auth(session=session)
def updateSystemStatus(update):
    # TODO: add documentation
    changeStatus(json.loads(update))
    show_service_info()


@socketio.on('systemUsers')
@socket_auth(session=session)
def systemUsers(empty=None):
    systemUserArray = DatabaseController().query_systemUser()
    jsondata = {"SystemUsers": []}
    for user in systemUserArray:
        userjson = {}
        userjson['Name'] = user.name
        userjson["Group"] = user.group
        userjson["Token"] = user.token
        userjson["Password"] = user.password
        userjson["Certs"] = user.certificate_package_name
        userjson["Uid"] = user.uid
        jsondata["SystemUsers"].append(userjson)

    emit('systemUsersUpdate', json.dumps(jsondata))


@socketio.on('addSystemUser')
@socket_auth(session=session)
def addSystemUser(jsondata):
    from FreeTAKServer.controllers import certificate_generation
    import uuid
    for systemuser in json.loads(jsondata)['systemUsers']:
        if systemuser["Certs"] == "true":
            # create certs
            certificate_generation.AtakOfTheCerts().bake(cn=systemuser["Name"])
            certificate_generation.generate_zip(user_filename=systemuser["Name"] + '.p12')
            # add DP
            import string
            from pathlib import PurePath, Path
            import hashlib
            import shutil
            import os
            dp_directory = str(PurePath(Path(MainConfig.DataPackageFilePath)))
            letters = string.ascii_letters
            openfile = open(str(PurePath(Path(str(MainConfig.clientPackages), systemuser["Name"] + '.zip'))), mode='rb')
            file_hash = str(hashlib.sha256(openfile.read()).hexdigest())
            openfile.close()
            newDirectory = str(PurePath(Path(dp_directory), Path(file_hash)))
            os.mkdir(newDirectory)
            shutil.copy(str(PurePath(Path(str(MainConfig.clientPackages), systemuser["Name"] + '.zip'))),
                        str(PurePath(Path(newDirectory), Path(systemuser["Name"] + '.zip'))))
            fileSize = Path(str(newDirectory), systemuser["Name"] + '.zip').stat().st_size
            dbController.create_datapackage(uid=str(uuid.uuid4()), Name=systemuser["Name"] + '.zip', Hash=file_hash,
                                            SubmissionUser='server',
                                            CreatorUid='server-uid', Size=fileSize, Privacy=1)
            DatabaseController().create_systemUser(name=systemuser["Name"], group=systemuser["Group"],
                                                   token=systemuser["Token"], password=systemuser["Password"],
                                                   uid=str(uuid.uuid4()), certificate_package_name=systemuser["Name"] + '.zip')
            import datetime as dt
            DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            add = dt.timedelta(seconds=600)
            stale_part = dt.datetime.strptime(zulu, DATETIME_FMT) + add
            stale = stale_part.strftime(DATETIME_FMT)
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            time = zulu
            from FreeTAKServer.controllers.SpecificCoTControllers.SendOtherController import SendOtherController
            from FreeTAKServer.model.RawCoT import RawCoT
            cot = RawCoT()
            clientXML = f'<?xml version="1.0"?><event version="2.0" uid="{str(uuid.uuid4())}" type="b-f-t-r" time="{time}" start="{time}" stale="{stale}" how="h-e"><point lat="43.85570300" lon="-66.10801200" hae="19.55866360" ce="3.21600008" le="nan" /><detail><fileshare filename="{systemuser["Name"]}" senderUrl="{MainConfig.DataPackageServiceDefaultIP}:8080/Marti/api/sync/metadata/{str(file_hash)}/tool" sizeInBytes="{fileSize}" sha256="{str(file_hash)}" senderUid="{"server-uid"}" senderCallsign="{"server"}" name="{systemuser["Name"]+".zip"}" /><ackrequest uid="{uuid.uuid4()}" ackrequested="true" tag="{systemuser["Name"]+".zip"}" /><marti><dest callsign="{systemuser["Name"]}" /></marti></detail></event>'
            cot.xmlString = clientXML.encode()
            newCoT = SendOtherController(cot)
            APIPipe.send(newCoT.getObject())

        else:
            DatabaseController().create_systemUser(name=systemuser["Name"], group=systemuser["Group"],
                                                   token=systemuser["Token"], password=systemuser["Password"],
                                                   uid=str(uuid.uuid4()))


@socketio.on("removeSystemUser")
@socket_auth(session=session)
def removeSystemUser(jsondata):
    jsondata = json.loads(jsondata)
    for systemUser in jsondata["systemUsers"]:
        uid = systemUser["uid"]
        systemUser = dbController.query_systemUser(query=f'uid == "{uid}"')[0]
        certificate_package_name = systemUser.certificate_package_name
        dbController.remove_systemUser(f'uid == "{uid}"')
        obj = dbController.query_datapackage(f'Name == "{certificate_package_name}"')
        # TODO: make this coherent with constants
        currentPath = MainConfig.DataPackageFilePath
        shutil.rmtree(f'{str(currentPath)}/{obj[0].Hash}')
        dbController.remove_datapackage(f'Hash == "{obj[0].Hash}"')


@socketio.on("events")
@socket_auth(session=session)
def events(empty=None):
    return socketio.emit("eventsUpdate", {"events": ["system user ALPHA created", "SSL DataPackage Service turned off", "TCP CoT Service port changed to 8086", "Outgoing Federation created to 1.1.1.1", "Federate connected from 0.0.0.0"]})


@app.route("/SendGeoChat", methods=[restMethods.POST])
@auth.login_required()
def SendGeoChat():
    try:
        json = request.json
        modelObject = Event.GeoChat()
        out = ApplyFullJsonController().serializeJsonToModel(modelObject, json)
        xml = XMLCoTController().serialize_model_to_CoT(out, 'event')
        from FreeTAKServer.controllers.SpecificCoTControllers.SendGeoChatController import SendGeoChatController
        rawcot = RawCoT()
        rawcot.xmlString = xml
        rawcot.clientInformation = None
        object = SendGeoChatController(rawcot)
        APIPipe.send(object.getObject())
        return '200', 200
    except Exception as e:
        print(e)

# public API endpoints


@app.route("/ManagePresence")
@auth.login_required()
def ManagePresence():
    pass


@app.route("/ManagePresence/postPresence", methods=[restMethods.POST])
@auth.login_required
def postPresence():
    try:
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_presence_post(jsondata)
        Presence = SendPresenceController(jsonobj).getCoTObject()
        APIPipe.send(Presence)
        return Presence.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 500


@app.route("/ManageGeoObject")
@auth.login_required()
def ManageGeoObject():
    pass


@app.route("/ManageGeoObject/postGeoObject", methods=[restMethods.POST])
@auth.login_required
def postGeoObject():
    try:
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_geoobject_post(jsondata)
        simpleCoTObject = SendSimpleCoTController(jsonobj).getCoTObject()
        APIPipe.send(simpleCoTObject)
        return simpleCoTObject.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 500


@app.route("/ManageChat")
@auth.login_required()
def ManageChat():
    pass


@app.route("/ManageChat/postChatToAll", methods=[restMethods.POST])
@auth.login_required
def postChatToAll():
    try:
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_chat_post(jsondata)
        ChatObject = SendChatController(jsonobj).getCoTObject()
        APIPipe.send(ChatObject)
        return 'success', 200
    except Exception as e:
        return str(e), 500


@app.route("/ManageEmergency/getEmergency", methods=[restMethods.GET])
@auth.login_required
def getEmergency():
    try:
        output = dbController.query_ActiveEmergency()
        for i in range(0, len(output)):
            original = output[i]
            output[i] = output[i].__dict__
            output[i]["lat"] = original.event.point.lat
            output[i]["lon"] = original.event.point.lon
            output[i]["type"] = original.event.detail.emergency.type
            output[i]["name"] = original.event.detail.contact.callsign
            del (output[i]['_sa_instance_state'])
            del(output[i]['event'])
        return jsonify(json_list=output), 200
    except Exception as e:
        return str(e), 200


@app.route("/ManageEmergency/postEmergency", methods=[restMethods.POST])
@auth.login_required
def postEmergency():
    try:
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_emergency_post(jsondata)
        EmergencyObject = SendEmergencyController(jsonobj).getCoTObject()
        APIPipe.send(EmergencyObject)
        return EmergencyObject.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 200


@app.route("/ManageEmergency/deleteEmergency", methods=[restMethods.DELETE])
@auth.login_required
def deleteEmergency():
    try:
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_emergency_delete(jsondata)
        EmergencyObject = SendEmergencyController(jsonobj).getCoTObject()
        APIPipe.send(EmergencyObject)
        return 'success', 200
    except Exception as e:
        return str(e), 500


@app.route("/ManageEmergency")
@auth.login_required
def Emergency():
    pass

# @app.route("/ConnectionMessage", methods=[restMethods.POST])


def ConnectionMessage():

    try:
        json = request.json
        modelObject = Event.GeoChat()
        out = ApplyFullJsonController().serializeJsonToModel(modelObject, json)
        xml = XMLCoTController().serialize_model_to_CoT(out, 'event')
        from FreeTAKServer.controllers import SendGeoChatController
        rawcot = RawCoT()
        rawcot.xmlString = xml
        rawcot.clientInformation = None
        object = SendGeoChatController(rawcot).getObject()
        object.type = "connmessage"
        APIPipe.send(object.SendGeoChat)
        return '200', 200
    except Exception as e:
        print(e)


@app.route("/APIUser", methods=[restMethods.GET, restMethods.POST, restMethods.DELETE])
def APIUser():
    if request.remote_addr in MainConfig.AllowedCLIIPs:
        try:
            if request.method == restMethods.POST:
                json = request.get_json()
                dbController.create_APIUser(Username=json['username'], Token=json['token'])
                return 'success', 200

            elif request.method == restMethods.DELETE:
                json = request.get_json()
                username = json['username']
                dbController.remove_APIUser(query=f'Username == "{username}"')
                return 'success', 200

            elif request.method == restMethods.GET:
                output = dbController.query_APIUser()
                for i in range(0, len(output)):
                    output[i] = output[i].__dict__
                    del (output[i]['_sa_instance_state'])
                    del (output[i]['PrimaryKey'])
                    del (output[i]['uid'])
                return jsonify(json_list=output), 200

        except Exception as e:
            return str(e), 500
    else:
        return 'endpoint can only be accessed by approved IPs', 401


@app.route("/RecentCoT", methods=[restMethods.GET])
def RecentCoT():
    import time
    time.sleep(10)
    return b'1234'


@app.route("/URL", methods=[restMethods.GET])
def URLGET():
    data = request.args
    print(data)
    return 'completed', 200


@app.route("/Clients", methods=[restMethods.GET])
def Clients():
    try:
        if request.remote_addr in MainConfig.AllowedCLIIPs:
            CommandPipe.send([functionNames.Clients])
            out = CommandPipe.recv()
            returnValue = []
            for client in out:
                returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
            dumps = json.dumps(returnValue)
            return dumps
        else:
            return 'endpoint can only be accessed by approved IPs', 401
    except Exception as e:
        return str(e), 500


@app.route('/FederationTable', methods=[restMethods.GET, restMethods.POST, "PUT", restMethods.DELETE])
@auth.login_required()
def FederationTable():
    try:
        if request.method == restMethods.GET:
            output = dbController.query_ActiveFederation()
            for i in range(0, len(output)):
                output[i] = output[i].__dict__
                del (output[i]['_sa_instance_state'])
            output2 = dbController.query_Federation()
            for i in range(0, len(output2)):
                output2[i] = output2[i].__dict__
                del (output2[i]['_sa_instance_state'])

            return jsonify(activeFederations=output, federations=output2), 200

        elif request.method == restMethods.POST:
            import uuid
            jsondata = json.loads(request.data)
            new_outgoing_federations = jsondata["outgoingFederations"]
            for new_fed in new_outgoing_federations:
                id = str(uuid.uuid4())
                dbController.create_Federation(**new_fed, id=id)
                if new_fed["status"] == "Enabled":
                    CommandPipe.send((id, "CREATE"))
                else:
                    pass
            return '', 200

        elif request.method == "PUT":
            jsondata = json.loads(request.data)
            federations = jsondata["federations"]
            for fed in federations:
                old_fed = dbController.query_Federation(f'id == "{fed["id"]}"')[0]
                old_status = old_fed.status
                old_id = old_fed.id
                dbController.update_Federation(column_value=fed, query=f'id == "{fed["id"]}"')
                if "status" in fed:
                    if fed["status"] == "Enabled":

                        if old_status != "Enabled":
                            CommandPipe.send((old_id, "CREATE"))
                        else:
                            pass
                    elif fed["status"] == "Disabled":
                        if old_status != "Disabled":
                            CommandPipe.send((old_id, "DELETE"))
                        else:
                            pass
                    else:
                        pass
            return '', 200

        elif request.method == "DELETE":
            jsondata = json.loads(request.data)
            federations = jsondata["federations"]
            for fed in federations:
                fedInstance = dbController.query_Federation(f'id == "{fed["id"]}"')[0]
                if fedInstance.status == "Enabled":
                    CommandPipe.send((fed.id, "DELETE"))
                else:
                    pass
                dbController.remove_Federation(f'id == "{fed["id"]}"')
            return '', 200

    except Exception as e:
        return str(e), 500


@app.route('/DataPackageTable', methods=[restMethods.GET, restMethods.POST, restMethods.DELETE, "PUT"])
@auth.login_required()
def DataPackageTable():
    if request.method == "GET":
        output = dbController.query_datapackage()
        for i in range(0, len(output)):
            output[i] = output[i].__dict__
            del (output[i]['_sa_instance_state'])
            del (output[i]['CreatorUid'])
            del (output[i]['MIMEType'])
            del (output[i]['uid'])
        return jsonify(json_list=output), 200

    elif request.method == "DELETE":
        jsondata = json.loads(request.data)
        Hashes = jsondata['DataPackages']
        for hash in Hashes:
            Hash = hash['hash']
            print(Hash)
            obj = dbController.query_datapackage(f'Hash == "{Hash}"')
            print(obj)
            # TODO: make this coherent with constants
            currentPath = MainConfig.DataPackageFilePath
            shutil.rmtree(f'{str(currentPath)}/{obj[0].Hash}')
            dbController.remove_datapackage(f'Hash == "{Hash}"')
        return '200', 200

    elif request.method == "POST":
        dp_directory = str(PurePath(Path(MainConfig.DataPackageFilePath)))
        letters = string.ascii_letters
        uid = str(uuid.uuid4())
        filename = request.args.get('filename')
        creatorUid = request.args.get('creatorUid')
        file = request.files.getlist('assetfile')[0]
        with ZipFile(file, mode='a') as zip:
            if "MANIFEST/manifest.xml" in [member.filename for member in zip.infolist()]:
                manifestXML = etree.Element("MissionPackageManifest", version="2")
                config = etree.SubElement(manifestXML, "Configuration")
                etree.SubElement(config, "Parameter", name="uid", value=uid)
                etree.SubElement(config, "Parameter", name="name", value=filename)

                contents = etree.SubElement(manifestXML, "Contents")
                for fileName in zip.namelist():
                    etree.SubElement(contents, "Content", ignore="false", zipEntry=str(fileName))
                # manifest = zip.open('MANIFEST\\manifest.xml', mode="w")
                zip.writestr('MANIFEST\\manifest.xml', etree.tostring(manifestXML))
                print(zip.namelist())
                file.seek(0)
            else:
                pass

        tempuid = str(uuid.uuid4())
        app.logger.info(f"Data Package hash = {str(tempuid)}")
        directory = Path(dp_directory, tempuid)
        if not Path.exists(directory):
            os.mkdir(str(directory))
        file.seek(0)
        filepath = str(PurePath(Path(directory), Path(filename)))
        file.save(filepath)
        openfile = open(str(PurePath(Path(str(directory), filename))), mode='rb')
        file_hash = str(hashlib.sha256(openfile.read()).hexdigest())
        openfile.close()
        newDirectory = str(PurePath(Path(dp_directory), Path(file_hash)))
        os.rename(str(PurePath(Path(directory))), newDirectory)
        fileSize = Path(str(newDirectory), filename).stat().st_size
        if creatorUid is None:
            callsign = str(dbController.query_user(query='uid == "server-uid"', column=[
                'callsign']))  # fetchone() gives a tuple, so only grab the first element
            dbController.create_datapackage(uid=uid, Name=filename, Hash=file_hash, SubmissionUser='server',
                                            CreatorUid='server-uid', Size=fileSize)
        else:
            callsign = str(dbController.query_user(query=f'uid == f"{creatorUid}"', column=[
                'callsign']))  # fetchone() gives a tuple, so only grab the first element
            dbController.create_datapackage(uid=uid, Name=filename, Hash=file_hash, SubmissionUser=callsign,
                                            CreatorUid=creatorUid, Size=fileSize)
        return 'successful', 200

    elif request.method == "PUT":
        updatedata = json.loads(request.data)
        DataPackages = updatedata['DataPackages']
        for dp in DataPackages:
            updateDict = {}
            if 'Privacy' in dp:
                updateDict["Privacy"] = int(dp["Privacy"])
            if "Keywords" in dp:
                updateDict["Keywords"] = dp["Keywords"]
            if "Name" in dp:
                updateDict["Name"] = dp["Name"]
            dbController.update_datapackage(query=f'PrimaryKey == {dp["PrimaryKey"]}', column_value=updateDict)
        return "success", 200


def getMission():
    import uuid
    import random
    creator_uid = str(uuid.uuid4())
    maincontent = {
        "name": "some name",
        "description": "some description",
        "chatRoom": "",
        "tool": "public",
        "keywords": ["optional", "set", "of", "keywords"],
        "creatorUid": creator_uid,
        "createTime": "2020-12-09T15:53:42.873Z",
        "groups": ["Allowed", "groups"],
        "externalData": [],
        "uids": [{
            "data": str(uuid.uuid4()),
            "timestamp": "2020-12-09T15:58:10.635Z",
            "creatorUid": creator_uid,
            "details": {
                "type": "a-h-G",
                "callsign": "R.9.155734",
                "iconsetPath": "COT_MAPPING_2525B/a-h/a-h-G"
            }
        }
        ],
        "contents": [{
            "data": {
                "filename": "name of file",
                "keywords": [],
                "mimeType": "application/octet-stream",
                "name": "name of mission",
                "submissionTime": "2020-12-09T15:55:21.468Z",
                "submitter": "submitter name",
                "uid": str(uuid.uuid4()),
                "hash": str(random.getrandbits(128)),
                "size": random.randint(1000, 100000)
            },
            "timestamp": "2020-12-09T15:55:21.559Z",
            "creatorUid": creator_uid
        }
        ],
        "passwordProtected": random.choice(['true', 'false'])
    }
    return maincontent


@app.route("/MissionTable", methods=['GET', 'POST', 'DELETE'])
@auth.login_required()
def mission_table():
    try:
        if request.method == "GET":
            jsondata = {
                "version": "3",
                "type": "Mission",
                "data": [],
                "nodeId": "6ff99444fa124679a3943ee90308a44c9d794c02-e5a5-42b5-b4c8-625203ea1287"
            }
            return json.dumps(jsondata)
        elif request.method == "POST":
            return b'', 200
        elif request.method == "DELETE":
            return b'', 200
    except Exception as e:
        return e, 500


@app.route("/ExCheckTable", methods=["GET", "POST", "DELETE"])
@auth.login_required()
def excheck_table():
    try:
        from pathlib import PurePath, Path
        from datetime import datetime
        from flask import request
        if request.method == "GET":
            jsondata = {"ExCheck": {'Templates': [], 'Checklists': []}}
            from FreeTAKServer.controllers.ExCheckControllers.templateToJsonSerializer import templateSerializer
            excheckTemplates = DatabaseController().query_ExCheck()
            for template in excheckTemplates:
                templateData = template.data
                templatejson = {
                    "filename": templateData.filename,
                    "name": templateData.keywords.name,
                    "submissionTime": templateData.submissionTime,
                    "submitter": str(dbController.query_user(query=f'uid == "{template.creatorUid}"', column=['callsign'])),
                    "uid": templateData.uid,
                    "hash": templateData.hash,
                    "size": templateData.size,
                    "description": templateData.keywords.description
                }
                jsondata["ExCheck"]['Templates'].append(templatejson)
            excheckChecklists = DatabaseController().query_ExCheckChecklist()
            for checklist in excheckChecklists:
                try:
                    templatename = checklist.template.data.name
                except AttributeError:
                    templatename = "template removed"
                checklistjson = {
                    "filename": checklist.filename,
                    "name": checklist.name,
                    "startTime": datetime.strftime(checklist.startTime, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    "submitter": checklist.callsign,
                    "uid": checklist.uid,
                    "description": checklist.description,
                    "template": templatename
                }
                jsondata["ExCheck"]['Checklists'].append(checklistjson)
            return json.dumps(jsondata), 200

        elif request.method == "DELETE":
            jsondata = request.data
            ExCheckArray = json.loads(jsondata)["ExCheck"]
            for item in ExCheckArray["Templates"]:
                templateitem = DatabaseController().query_ExCheck(f'ExCheckData.uid == "{item["uid"]}"', verbose=True)[0]
                os.remove(str(PurePath(Path(MainConfig.ExCheckFilePath), Path(templateitem.data.filename))))
                DatabaseController().remove_ExCheck(f'PrimaryKey == "{templateitem.PrimaryKey}"')
            for item in ExCheckArray["Checklists"]:
                checklistitem = DatabaseController().query_ExCheckChecklist(f'uid == "{item["uid"]}"')[0]
                os.remove(str(PurePath(Path(MainConfig.ExCheckChecklistFilePath), Path(checklistitem.filename))))
                DatabaseController().remove_ExCheckChecklist(f'uid == "{item["uid"]}"')
            return 'success', 200
        elif request.method == "POST":
            try:
                import uuid
                from FreeTAKServer.controllers.ExCheckControllers.templateToJsonSerializer import templateSerializer
                xmlstring = f'<?xml version="1.0"?><event version="2.0" uid="{uuid.uuid4()}" type="t-x-m-c" time="2020-11-28T17:45:51.000Z" start="2020-11-28T17:45:51.000Z" stale="2020-11-28T17:46:11.000Z" how="h-g-i-g-o"><point lat="0.00000000" lon="0.00000000" hae="0.00000000" ce="9999999" le="9999999" /><detail><mission type="CHANGE" tool="ExCheck" name="exchecktemplates" authorUid="S-1-5-21-2720623347-3037847324-4167270909-1002"><MissionChanges><MissionChange><contentResource><filename>61b01475-ad44-4300-addc-a9474ebf67b0.xml</filename><hash>018cd5786bd6c2e603beef30d6a59987b72944a60de9e11562297c35ebdb7fd6</hash><keywords>test init</keywords><keywords>dessc init</keywords><keywords>FEATHER</keywords><mimeType>application/xml</mimeType><name>61b01475-ad44-4300-addc-a9474ebf67b0</name><size>1522</size><submissionTime>2020-11-28T17:45:47.980Z</submissionTime><submitter>wintak</submitter><tool>ExCheck</tool><uid>61b01475-ad44-4300-addc-a9474ebf67b0</uid></contentResource><creatorUid>S-1-5-21-2720623347-3037847324-4167270909-1002</creatorUid><missionName>exchecktemplates</missionName><timestamp>2020-11-28T17:45:47.983Z</timestamp><type>ADD_CONTENT</type></MissionChange></MissionChanges></mission></detail></event>'
                # this is where the client will post the xmi of a template
                from datetime import datetime
                from lxml import etree
                import hashlib
                # possibly the uid of the client submitting the template
                authoruid = request.args.get('clientUid')
                if not authoruid:
                    authoruid = 'server-uid'
                XMI = request.data.decode()
                serializer = templateSerializer(XMI)
                object = serializer.convert_template_to_object()
                object.timestamp = datetime.strptime(object.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                serializer.create_DB_object(object)
                xml = etree.fromstring(XMI)
                path = str(PurePath(Path(MainConfig.ExCheckFilePath), Path(f'{object.data.uid}.xml')))
                with open(path, 'w+') as file:
                    file.write(XMI)
                    file.close()

                uid = object.data.uid
                temp = etree.fromstring(XMI)
                cot = etree.fromstring(xmlstring)
                cot.find('detail').find('mission').set("authorUid", authoruid)
                resources = cot.find('detail').find('mission').find('MissionChanges').find('MissionChange').find(
                    'contentResource')
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
                APIPipe.send(object)
                return str(uid), 200
            except Exception as e:
                print(str(e))
    except Exception as e:
        return str(e), 500


@app.route('/checkStatus', methods=[restMethods.GET])
@auth.login_required()
def check_status():
    try:
        if request.remote_addr in MainConfig.AllowedCLIIPs:
            CommandPipe.send([functionNames.checkStatus])
            FTSServerStatusObject = CommandPipe.recv()
            out = ApplyFullJsonController().serialize_model_to_json(FTSServerStatusObject)
            return json.dumps(out), 200
        else:
            return 'endpoint can only be accessed by approved IPs', 401
    except Exception as e:
        return str(e), 500

# @app.route('/changeStatus', methods=[restMethods.POST])
# @auth.login_required()


def changeStatus(jsonmessage):
    # TODO: modify to better support format
    mappings = {"on": "start", "off": "stop", "": ""}
    try:
        import json
        if not jsonmessage:
            jsonmessage = json.loads(request.data)
        FTSObject = FTS()
        json = jsonmessage["services"]
        ip = jsonmessage.get("ip")
        if jsonVars.COTSERVICE in json:
            CoTService = json[jsonVars.COTSERVICE]
            FTSObject.CoTService.CoTServiceIP = ip
            try:
                FTSObject.CoTService.CoTServicePort = int(CoTService.get(jsonVars.PORT))
            except BaseException:
                FTSObject.CoTService.CoTServicePort = ''
            FTSObject.CoTService.CoTServiceStatus = mappings[CoTService.get("status")]
        else:
            pass

        if jsonVars.DATAPACKAGESERVICE in json:

            DPService = json.get(jsonVars.DATAPACKAGESERVICE)
            FTSObject.TCPDataPackageService.TCPDataPackageServiceIP = ip
            try:
                FTSObject.TCPDataPackageService.TCPDataPackageServicePort = int(DPService.get(jsonVars.PORT))
            except BaseException:
                FTSObject.TCPDataPackageService.TCPDataPackageServicePort = ''
            FTSObject.TCPDataPackageService.TCPDataPackageServiceStatus = mappings[DPService.get("status")]

        else:
            pass

        if jsonVars.SSLDATAPACKAGESERVICE in json:

            DPService = json.get(jsonVars.SSLDATAPACKAGESERVICE)
            FTSObject.SSLDataPackageService.SSLDataPackageServiceIP = ip
            try:
                FTSObject.SSLDataPackageService.SSLDataPackageServicePort = int(DPService.get(jsonVars.PORT))
            except BaseException:
                FTSObject.SSLDataPackageService.SSLDataPackageServicePort = ''
            FTSObject.SSLDataPackageService.SSLDataPackageServiceStatus = mappings[DPService.get("status")]

        else:
            pass

        if jsonVars.SSLCOTSERVICE in json:

            SSLCoTservice = json[jsonVars.SSLCOTSERVICE]
            FTSObject.SSLCoTService.SSLCoTServiceIP = ip
            try:
                FTSObject.SSLCoTService.SSLCoTServicePort = int(SSLCoTservice.get(jsonVars.PORT))
            except BaseException:
                FTSObject.SSLCoTService.SSLCoTServicePort = ''
            FTSObject.SSLCoTService.SSLCoTServiceStatus = mappings[SSLCoTservice.get("status")]

        else:
            pass

        if jsonVars.FEDERATIONSERVERSERVICE in json:

            FederationServerService = json.get(jsonVars.FEDERATIONSERVERSERVICE)
            FTSObject.FederationServerService.FederationServerServiceIP = ip
            try:
                FTSObject.FederationServerService.FederationServerServicePort = int(FederationServerService.get(jsonVars.PORT))
            except BaseException:
                FTSObject.FederationServerService.FederationServerServicePort = ''
            FTSObject.FederationServerService.FederationServerServiceStatus = mappings[FederationServerService.get('status')]

        else:
            pass

        if jsonVars.RESTAPISERVICE in json:

            RESTAPISERVICE = json.get(jsonVars.RESTAPISERVICE)
            FTSObject.RestAPIService.RestAPIServiceIP = ip
            try:
                FTSObject.RestAPIService.RestAPIServicePort = int(RESTAPISERVICE.get(jsonVars.PORT))
            except BaseException:
                FTSObject.RestAPIService.RestAPIServicePort = ''
            FTSObject.RestAPIService.RestAPIServiceStatus = mappings[RESTAPISERVICE.get("status")]

        else:
            pass

            CommandPipe.send([functionNames.Status, FTSObject])
            out = CommandPipe.recv()
            return '200', 200

    except Exception as e:
        return '500', 500


def receiveUpdates():
    while True:
        try:
            update = APIPipe.recv()
            global UpdateArray
            UpdateArray.append(update)
        except Exception as e:
            print(e)


def submitData(dataRaw):
    global APIPipe
    print(APIPipe)
    data = RawCoT()
    data.clientInformation = "SERVER"
    data.xmlString = dataRaw.encode()
    APIPipe.send([data])


def emitUpdates(Updates):
    data = [SimpleClient()]
    data[0].callsign = ''
    data[0].team = ''
    data[0].ip = ''
    returnValue = []
    for client in data:
        returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
    socketio.emit('up', json.dumps(returnValue), broadcast=True)
    data = Updates
    for client in data:
        returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
    socketio.emit('up', json.dumps(returnValue), broadcast=True)
    return 1


def test(json):
    modelObject = Event.dropPoint()
    out = XMLCoTController().serialize_CoT_to_model(modelObject, etree.fromstring(json))
    xml = XMLCoTController().serialize_model_to_CoT(out, 'event')
    from FreeTAKServer.controllers.SpecificCoTControllers.SendDropPointController import SendDropPointController
    rawcot = RawCoT()
    rawcot.xmlString = xml
    rawcot.clientInformation = None
    object = SendDropPointController(rawcot)
    print(etree.tostring(object.sendDropPoint.xmlString, pretty_print=True).decode())
    '''EventObject = json
    modelObject = ApplyFullJsonController(json, 'Point', modelObject).determine_function()
    out = XMLCoTController().serialize_model_to_CoT(modelObject, 'event')
    print(etree.tostring(out))
    print(RestAPI().serializeJsonToModel(modelObject, EventObject))'''


class RestAPI:
    def __init__(self):
        pass

    def startup(self, APIPipea, CommandPipea, IP, Port, starttime):
        global APIPipe, CommandPipe, StartTime
        StartTime = starttime
        APIPipe = APIPipea
        CommandPipe = CommandPipea
        threading.Thread(target=receiveUpdates, daemon=True, args=()).start()
        socketio.run(app, host=IP, port=Port)
        # try below if something breaks
        # socketio.run(app, host='0.0.0.0', port=10984, debug=True, use_reloader=False)

    def serializeJsonToModel(self, model, Json):
        for key, value in Json.items():
            if isinstance(value, dict):
                submodel = getattr(model, key)
                out = self.serializeJsonToModel(submodel, value)
                setattr(model, key, out)
            else:
                setattr(model, key, value)
        return model


if __name__ == '__main__':
    excheck_table()
    #    app.run(host="127.0.0.1", port=80)
