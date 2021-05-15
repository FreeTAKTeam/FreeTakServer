from flask import Flask, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_cors import CORS

import json

from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables as vars

functionNames = vars()
functionNames.function_names()
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, async_handlers=True, async_mode="eventlet")
socketio.init_app(app, cors_allowed_origins="*")
dbController = DatabaseController()

def startup(self, APIPipea, CommandPipea, IP, Port, starttime):
    global APIPipe, CommandPipe, StartTime
    StartTime = starttime
    APIPipe = APIPipea
    CommandPipe = CommandPipea
    socketio.run(app, host=IP, port=Port)

def socket_auth(session = None):
    def innerfunc(x):
        def wrapper(*args, **kwargs):
            if hasattr(session, 'authenticated') and session.authenticated:
                x(*args, **kwargs)
            else:
                pass

        return wrapper

    return innerfunc

@socketio.on('connect')
def connection():
    emit('connectUpdate', jsonify(starttime=str(StartTime), version= str(MainConfig.version)))


@socketio.on('authenticate')
def authenticate(token):
    if json.loads(token)["Authenticate"] == "a@v{5]MQU><waQ;Z":
        emit('authentication', json.dumps({'successful': 'True'}))
        session.authenticated = True
    else:
        emit('authentication', json.dumps({'successful': 'False'}))


@socketio.on('users')
@socket_auth(session = session)
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
            except:
                output[i]['callsign'] = "undefined"
                output[i]['team'] = "undefined"
            del (output[i]['_sa_instance_state'])
            del (output[i]['CoT_id'])
            del (output[i]['CoT'])
        except Exception as e:
            print(e)
    socketio.emit('userUpdate', json.dumps({"Users": output}))

@socketio.on('logs')
@socket_auth(session = session)
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
@socket_auth(session = session)
def show_service_info(empty=None):
    mapping = {"start": "on", "stop": "off", "":""}
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
    CommandPipe.put([functionNames.checkStatus])
    return CommandPipe.get()

@socketio.on("serverHealth")
@socket_auth(session = session)
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
            import random
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
                                                   uid=str(uuid.uuid4()), certificate_package_name=systemuser["Name"]+'.zip')
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
            APIPipe.put(newCoT.getObject())

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
