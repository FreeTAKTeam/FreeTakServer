from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_httpauth import HTTPTokenAuth
from flask_login import current_user, LoginManager
import threading
from functools import wraps
import uuid
import datetime as dt
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
import datetime
from defusedxml import ElementTree as etree
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
from FreeTAKServer.controllers.RestMessageControllers.SendDeleteVideoStreamController import SendDeleteVideoStreamController
import os
import shutil
import json
from flask_cors import CORS
from FreeTAKServer.controllers.RestMessageControllers.SendSimpleCoTController import SendSimpleCoTController, UpdateSimpleCoTController
from FreeTAKServer.controllers.RestMessageControllers.SendPresenceController import SendPresenceController, UpdatePresenceController
from FreeTAKServer.controllers.RestMessageControllers.SendEmergencyController import SendEmergencyController
from FreeTAKServer.controllers.RestMessageControllers.SendSensorDroneController import SendSensorDroneController
from FreeTAKServer.controllers.RestMessageControllers.SendSPISensorController import SendSPISensorController
from FreeTAKServer.controllers.RestMessageControllers.SendImageryVideoController import SendImageryVideoController
from FreeTAKServer.controllers.RestMessageControllers.SendRouteController import SendRouteController
from FreeTAKServer.controllers.RestMessageControllers.SendVideoStreamController import SendVideoStreamController
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
eventDict = {}

@app.errorhandler(404)
def page_not_found(e):
    return 'this endpoint does not exist'


@auth.verify_token
def verify_token(token):
    if token:
        output = dbController.query_APIUser(query=f'token = "{token}"')
        if output:
            return output[0].Username
        else:
            output = dbController.query_systemUser(query=f'token = "{token}"')
            if output:
                output = output[0]
                r = request
                dbController.create_APICall(user_id = output.uid, timestamp = dt.datetime.now(), content = request.data, endpoint = request.base_url)
                return output.name


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def socket_auth(session = None):
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
    if json.loads(token)["Authenticate"] == MainConfig.websocketkey:
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
    log_data = {'log_data': []}
    for line in reversed(open(LoggingConstants().ERRORLOG, "r").readlines()):
        try:
            timeoflog = line.split(" : ")[1]
            if datetime.datetime.strptime(timeoflog, '%Y-%m-%d %H:%M:%S,%f') > datetime.datetime.strptime(
                    json.loads(time)["time"], '%Y-%m-%d %H:%M:%S,%f'):
                outline = {"time": '', "type": '', 'file': '', 'message': ''}
                line_segments = line.split(" : ")
                outline["type"] = line_segments[0]
                outline["time"] = line_segments[1]
                outline["file"] = line_segments[2]
                outline["message"] = " : ".join(line_segments[3:-1])
                log_data['log_data'].append(outline)
            else:
                break
        except:
            pass
    for num in range(1, 6):
        try:
            for line in reversed(open(LoggingConstants().ERRORLOG+'.'+str(num), "r").readlines()):
                try:
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
                except:
                    pass
        except:
            pass
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
    out = CommandPipe.get()
    while hasattr(out, "CoTService") == False:
        out = CommandPipe.get()
    return out
@socketio.on("serverHealth")
@socket_auth(session = session)
def serverHealth(empty=None):
    import psutil
    import pathlib
    import os
    disk_usage = int(psutil.disk_usage(str(pathlib.Path(os.getcwd()).anchor)).percent)
    memory_usage = int(psutil.virtual_memory().percent)
    cpu_usage = int(psutil.cpu_percent(interval=0.1))
    jsondata = {
                "CPU": cpu_usage,
                "memory": memory_usage,
                "disk": disk_usage
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
@socket_auth(session=session)
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
    try:
        for systemuser in json.loads(jsondata)['systemUsers']:
            if systemuser["Certs"] == "true":
                # create certs
                certificate_generation.AtakOfTheCerts().bake(common_name=systemuser["Name"])
                certificate_generation.generate_zip(user_filename=systemuser["Name"] + '.p12')
                # add DP
                import string
                import random
                from pathlib import PurePath, Path
                import hashlib
                from defusedxml import ElementTree as etree
                import shutil
                import os
                dp_directory = str(PurePath(Path(MainConfig.DataPackageFilePath)))
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
                dbController.create_systemUser(name=systemuser["Name"], group=systemuser["Group"],
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
                DPIP = getStatus().TCPDataPackageService.TCPDataPackageServiceIP
                clientXML = f'<?xml version="1.0"?><event version="2.0" uid="{str(uuid.uuid4())}" type="b-f-t-r" time="{time}" start="{time}" stale="{stale}" how="h-e"><point lat="43.85570300" lon="-66.10801200" hae="19.55866360" ce="3.21600008" le="nan" /><detail><fileshare filename="{systemuser["Name"]}" senderUrl="{DPIP}:8080/Marti/api/sync/metadata/{str(file_hash)}/tool" sizeInBytes="{fileSize}" sha256="{str(file_hash)}" senderUid="{"server-uid"}" senderCallsign="{"server"}" name="{systemuser["Name"]+".zip"}" /><ackrequest uid="{uuid.uuid4()}" ackrequested="true" tag="{systemuser["Name"]+".zip"}" /><marti><dest callsign="{systemuser["Name"]}" /></marti></detail></event>'
                cot.xmlString = clientXML.encode()
                newCoT = SendOtherController(cot, addToDB=False)
                APIPipe.put(newCoT.getObject())

            else:
                dbController.create_systemUser(name=systemuser["Name"], group=systemuser["Group"],
                                                       token=systemuser["Token"], password=systemuser["Password"],
                                                       uid=str(uuid.uuid4()))
    except Exception as e:
        print(e)
        return str(e), 500

@socketio.on("removeSystemUser")
@socket_auth(session=session)
def removeSystemUser(jsondata):
    from FreeTAKServer.controllers.certificate_generation import revoke_certificate
    jsondata = json.loads(jsondata)
    for systemUser in jsondata["systemUsers"]:
        uid = systemUser["uid"]
        systemUser = dbController.query_systemUser(query=f'uid = "{uid}"')[0]
        na = systemUser.name
        revoke_certificate(username = na)
        certificate_package_name = systemUser.certificate_package_name
        dbController.remove_systemUser(f'uid = "{uid}"')
        obj = dbController.query_datapackage(f'Name = "{certificate_package_name}"')
        # TODO: make this coherent with constants
        currentPath = MainConfig.DataPackageFilePath
        shutil.rmtree(f'{str(currentPath)}/{obj[0].Hash}')
        dbController.remove_datapackage(f'Hash = "{obj[0].Hash}"')
        os.remove(MainConfig.certsPath+f"/{na}.pem")
        os.remove(MainConfig.certsPath+f"/{na}.key")
        os.remove(MainConfig.certsPath+f"/{na}.p12")

@socketio.on("events")
@socket_auth(session=session)
def events(empty=None):
    current_notifications = Notification()
    #socketio.emit(json.dumps([current_notifications.logErrors, current_notifications.emergencys]))
    emit("eventsUpdate", {"events": current_notifications.logErrors+current_notifications.emergencys})

@app.route('/ManageNotification/getNotification', methods = ["GET"])
def notification():
    current_notifications = Notification()
    return json.dumps({"logErrors": current_notifications.logErrors, "emergencys": current_notifications.emergencys})


def getlogErrors():
    output = []
    for line in reversed(open(LoggingConstants().ERRORLOG, "r").readlines()):
        try:
            outline = {"time": '', "type": '', 'file': '', 'message': ''}
            line_segments = line.split(" : ")
            if line_segments[0] != "CRITICAL":
                continue
            outline["type"] = line_segments[0]
            outline["time"] = line_segments[1]
            outline["file"] = line_segments[2]
            if len(line_segments)> 4:
                outline["message"] = " : ".join(line_segments[3:-1])
            else:
                outline["message"] = line_segments[3]
            output.append(outline)
        except:
            pass
    for num in range(1, 6):
        try:
            for line in reversed(open(LoggingConstants().ERRORLOG + '.' + str(num), "r").readlines()):
                try:
                    timeoflog = line.split(" : ")[1]
                    outline = {"time": '', "type": '', 'file': '', 'message': ''}
                    line_segments = line.split(" : ")
                    if line_segments[0] != "CRITICAL":
                        continue
                    outline["type"] = line_segments[0]
                    outline["time"] = line_segments[1]
                    outline["file"] = line_segments[2]
                    outline["message"] = line_segments[3]
                    output.append(outline)
                except:
                    pass
        except:
            pass
    return output


def getemergencys():
    output = dbController.query_ActiveEmergency()
    for i in range(0, len(output)):
        try:
            original = output[i]
            output[i] = output[i].__dict__
            output[i]["lat"] = original.event.point.lat
            output[i]["lon"] = original.event.point.lon
            output[i]["type"] = original.event.detail.emergency.type
            output[i]["name"] = original.event.detail.contact.callsign
            del (output[i]['_sa_instance_state'])
            del (output[i]['event'])
        except:
            pass
    return output


class Notification:
    def __init__(self):
        try:
            self.emergencys = [i["name"]+" "+i["type"] for i in getemergencys()]
        except:
            self.emergencys = []
        try:
            self.logErrors = [i["message"] for i in getlogErrors()]
        except:
            self.logErrors = []

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
        APIPipe.put(object.getObject())
        return '200', 200
    except Exception as e:
        print(e)



@app.route("/ManagePresence")
@auth.login_required()
def ManagePresence():
    pass

@app.route("/ManagePresence/postPresence", methods=[restMethods.POST])
@auth.login_required
def postPresence():
    try:
        from json import dumps
        #jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'how': 'nonCoT', 'name': 'testing123'}
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_presence_post(jsondata)
        Presence = SendPresenceController(jsonobj).getCoTObject()
        APIPipe.put(Presence)
        return Presence.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 500

@app.route("/ManagePresence/putPresence", methods=["PUT"])
@auth.login_required
def putPresence():
    try:
        from json import dumps
        #jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'how': 'nonCoT', 'name': 'testing123'}
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_presence_post(jsondata)
        Presence = UpdatePresenceController(jsonobj).getCoTObject()
        APIPipe.put(Presence)
        return Presence.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 500

@app.route("/ManageRoute")
@auth.login_required()
def ManageRoute():
    pass

@app.route("/ManageRoute/postRoute", methods=["POST"])
def postRoute():
    try:
        from json import dumps
        #jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'how': 'nonCoT', 'name': 'testing123'}
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_route_post(jsondata)
        Route = SendRouteController(jsonobj).getCoTObject()
        APIPipe.put(Route)
        return Route.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 500

@app.route("/ManageCoT/getZoneCoT", methods=[restMethods.GET])
@auth.login_required
def getZoneCoT():
    try:
        from math import sqrt, degrees, cos, sin, radians, atan2
        from sqlalchemy import or_, and_
        jsondata = request.get_json(force=True)
        radius = int(jsondata["radius"])
        lat = (int(jsondata["latitude"]))
        lon = int(jsondata["longitude"])
        lat_abs = abs(lat)
        lon_abs = abs(lon)
        import geopy
        from geopy.distance import distance
        from FreeTAKServer.model.SQLAlchemy.CoTTables.Point import Point
        from FreeTAKServer.model.SQLAlchemy.Event import Event
        from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
        import re
        radius_in_deg = (geopy.units.degrees(arcseconds = geopy.units.nautical(meters=radius)))/2

        results = dbController.query_CoT(query= [Event.point.has(or_(and_(Point.lon<0, Point.lat<0, ((((Point.lon*-1)-lon_abs)*111302.62) + (((Point.lat*-1)-lat_abs)*110574.61)) <= radius+10), and_(Point.lon<0, Point.lat>=0, ((((Point.lon*-1)-lon_abs)*111302.62) + ((Point.lat-lat_abs)*110574.61)) <= radius+10), and_(Point.lon>=0, Point.lat<0, (((Point.lon-lon_abs)*111302.62) + (((Point.lat*-1)-lat_abs)*110574.61)) <= radius+10), and_(Point.lon>=0, Point.lat>=0, (((Point.lon-lon_abs)*111302.62) + ((Point.lat-lat_abs)*110574.61)) <= radius+10)))])
        print(results)
        output = []
        for result in results:
            try:
                dLon = (result.point.lon - lon)
                x = cos(radians(result.point.lat)) * sin(radians(dLon))
                y = cos(radians(lat)) * sin(radians(result.point.lat)) - sin(radians(lat)) * cos(radians(result.point.lat)) * cos(radians(dLon))
                brng = atan2(x, y)
                brng = degrees(brng)
                type_pattern = [type for type in list(RestEnumerations.supportedTypeEnumerations.values()) if re.fullmatch(type, result.type)][0]
                index_number = list(RestEnumerations.supportedTypeEnumerations.values()).index(type_pattern)
                type = list(RestEnumerations.supportedTypeEnumerations.keys())[index_number]
                print(type)
                part1 = result.type.split(type_pattern.split('.')[0])
                part2 = '-'+part1[1].split(type_pattern.split('.')[1])[0]+'-'
                attitude = list(RestEnumerations.attitude.keys())[list(RestEnumerations.attitude.values()).index(part2)]
                print(attitude)
                # attitude = RestEnumerations.attitude['-'+type.split(type_pattern.split('.')[0])[1].split(type_pattern.split('.')[1])+'-']

                output.append({"latitude": result.point.lat,
                               "longitude": result.point.lon,
                               "distance": distance((result.point.lon, result.point.lat), (lon, lat)).m,
                               "direction": brng,
                               "type": type,
                               "attitude": attitude
                               })
            except Exception as e:
                pass
        return json.dumps(output)
    except Exception as e:
        return str(e), 500

@app.route("/ManageGeoObject")
@auth.login_required()
def ManageGeoObject():
    pass

@app.route("/ManageGeoObject/getGeoObject", methods=[restMethods.GET])
@auth.login_required
def getGeoObject():
    try:
        from math import sqrt, degrees, cos, sin, radians, atan2
        from sqlalchemy import or_, and_
        # jsondata = request.get_json(force=True)
        radius = request.args.get("radius", default=100, type = int)
        lat = request.args.get("latitude", default=0, type = float)
        lon = request.args.get("longitude", default=0, type= float)
        expectedAttitude = request.args.get("attitude", default="*", type=str)
        lat_abs = lat
        lon_abs = lon
        import geopy
        from geopy.distance import distance
        from FreeTAKServer.model.SQLAlchemy.CoTTables.Point import Point
        from FreeTAKServer.model.SQLAlchemy.Event import Event
        from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
        import re
        radius_in_deg = (geopy.units.degrees(arcseconds=geopy.units.nautical(meters=radius))) / 2
        if lat_abs >= 0 and lon_abs >= 0:
            results = dbController.query_CoT(query=[Event.point.has(and_(
                    Point.lon >= 0,
                    Point.lat >= 0,
                    or_(
                        and_(
                            (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) <= radius + 10,
                            (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) > 0),
                        and_((
                            ((lon_abs - Point.lon) * 111302.62) + ((lon_abs - Point.lat) * 110574.61)) <= radius + 10,
                            (((lon_abs - Point.lon) * 111302.62) + ((lon_abs - Point.lat) * 110574.61)) > 0))))])
        elif lon_abs < 0 and lat_abs < 0:
            results = dbController.query_CoT(query=[Event.point.has(and_(
                Point.lon < 0,
                Point.lat < 0,
                or_(
                    and_(
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) > 0,
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) <= radius + 10),
                    and_(
                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) > 0,
                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) <= radius + 10)
                    )
                    ))])

        elif lon_abs < 0 and lat_abs > 0:
            results = dbController.query_CoT(query=[Event.point.has(and_(
                Point.lon < 0,
                Point.lat >= 0,
                or_(
                    and_(
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) <= radius + 10,
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) > 0),
                    and_(
                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) <= radius + 10,
                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) > 0)
                )))])

        elif lon_abs > 0 and lat_abs < 0:
            results = dbController.query_CoT(query=[Event.point.has(and_(
                Point.lon >= 0,
                Point.lat < 0,
                or_(

                    and_(

                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) <= radius + 10,
                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) > 0),
                    and_(

                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) <= radius + 10,
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) > 0))

                ))])

        else:
            return "unsupported coordinates"

        """                 and_(
                            Point.lon < 0,
                            Point.lat < 0,
                            ((((Point.lon * -1) - lon_abs) * 111302.62) + (((Point.lat * -1) - lat_abs) * 110574.61)) > 0,
                            ((((Point.lon * -1) - lon_abs) * 111302.62) + (((Point.lat * -1) - lat_abs) * 110574.61)) <= radius + 10),
            
                        and_(
                            Point.lon < 0,
                            Point.lat >= 0,
                            or_(
                                and_(
                                    ((((Point.lon * -1) - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) <= radius + 10,
                                    ((((Point.lon * -1) - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61))> 0),
                                and_(
                                    ((((lon_abs * -1) - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) <= radius + 10,
                                    ((((lon_abs * -1) - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) > 0)
                            ),
            
                        ),
                        and_(
                            Point.lon >= 0,
                            Point.lat < 0,
                            (((Point.lon - lon_abs) * 111302.62) + (((Point.lat * -1) - lat_abs) * 110574.61)) <= radius + 10,
                            (((Point.lon - lon_abs) * 111302.62) + (((Point.lat * -1) - lat_abs) * 110574.61))>0),"""

        print(results)
        output = []
        for result in results:
            try:
                print(result.uid)
                dLon = (result.point.lon - lon)
                x = cos(radians(result.point.lat)) * sin(radians(dLon))
                y = cos(radians(lat)) * sin(radians(result.point.lat)) - sin(radians(lat)) * cos(
                    radians(result.point.lat)) * cos(radians(dLon))
                brng = atan2(x, y)
                brng = degrees(brng)
                type_pattern = [type for type in list(RestEnumerations.supportedTypeEnumerations.values()) if
                                re.fullmatch(type, result.type)]
                print(type_pattern)
                type_pattern = type_pattern[0]
                index_number = list(RestEnumerations.supportedTypeEnumerations.values()).index(type_pattern)
                print(index_number)
                type = list(RestEnumerations.supportedTypeEnumerations.keys())[index_number]
                print(type)
                part1 = result.type.split(type_pattern.split('.')[0])
                part2 = '-' + part1[1].split(type_pattern.split('.')[1])[0] + '-'
                attitude = list(RestEnumerations.attitude.keys())[list(RestEnumerations.attitude.values()).index(part2)]
                if attitude == expectedAttitude or expectedAttitude == "*":
                    pass
                else:
                    continue
                print(attitude)
                # attitude = RestEnumerations.attitude['-'+type.split(type_pattern.split('.')[0])[1].split(type_pattern.split('.')[1])+'-']

                output.append({"latitude": result.point.lat,
                               "longitude": result.point.lon,
                               "distance": distance((result.point.lon, result.point.lat), (lon, lat)).m,
                               "direction": brng,
                               "type": type,
                               "attitude": attitude
                               })
            except Exception as e:
                print(e)
        return json.dumps(output)

    except Exception as e:
        return str(e), 500

@app.route("/ManageGeoObject/postGeoObject", methods=[restMethods.POST])
@auth.login_required
def postGeoObject():
    try:
        from geopy import Point, distance
        from json import dumps
        print("posting geo object")
        # jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'attitude': 'friend', 'geoObject': 'Ground', 'how': 'nonCoT', 'name': 'testing123'}
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_geoobject_post(jsondata)
        if "distance" in jsondata:
            start_point = Point(jsonobj.getlatitude(), jsonobj.getlongitude())
            d = distance.distance(meters=jsondata["distance"])
            if "bearing" in jsondata:
                end_point = d.destination(point=start_point, bearing=jsondata["bearing"])
            else:
                end_point = d.destination(point=start_point, bearing=360)
            jsonobj.setlatitude(end_point.latitude)
            jsonobj.setlongitude(end_point.longitude)

        simpleCoTObject = SendSimpleCoTController(jsonobj).getCoTObject()
        print("putting in queue")
        APIPipe.put(simpleCoTObject)
        print(simpleCoTObject.xmlString)
        print('put in queue')
        return simpleCoTObject.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 500

@app.route("/ManageGeoObject/putGeoObject", methods=["PUT"])
@auth.login_required
def putGeoObject():
    try:
        from json import dumps
        #jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'attitude': 'friend', 'geoObject': 'Ground', 'how': 'nonCoT', 'name': 'testing123'}
        jsondata = request.get_json(force=True)
        if "uid" in jsondata:
            jsonobj = JsonController().serialize_geoobject_post(jsondata)
            simpleCoTObject = UpdateSimpleCoTController(jsonobj).getCoTObject()
            simpleCoTObject.modelObject.setuid(jsondata["uid"])
            simpleCoTObject.setXmlString(XMLCoTController().serialize_model_to_CoT(simpleCoTObject.modelObject))
            APIPipe.put(simpleCoTObject)
            return simpleCoTObject.modelObject.getuid(), 200
        else:
            raise Exception("uid is a required parameter")
    except Exception as e:
        return str(e), 500

@app.route("/ManageVideoStream")
@auth.login_required()
def ManageVideoStream():
    pass

@app.route("/ManageVideoStream/getVideoStream", methods=[restMethods.GET])
@auth.login_required
def getVideoStream():
    try:
        from json import dumps
        from urllib import parse
        from FreeTAKServer.model.SQLAlchemy.CoTTables.Sensor import Sensor
        output = dbController.query_CoT(query='type="b-i-v" OR type="a-f-A-M-H-Q"')
        return_value = {"video_stream": []}
        for value in output:
            if value.detail._video.url:
                return_value["video_stream"].append(parse.urlparse(value.detail._video.url).path)
            elif value.detail._video.Connectionentry.path:
                return_value["video_stream"].append(value.detail._video.Connectionentry.path)
        return dumps(return_value), 200
    except Exception as e:
        return str(e), 500


@app.route("/ManageVideoStream/deleteVideoStream", methods=[restMethods.DELETE])
@auth.login_required
def deleteVideoStream():
    try:
        from json import dumps
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_video_stream_delete(jsondata)
        EmergencyObject = SendDeleteVideoStreamController(jsonobj).getCoTObject()
        APIPipe.put(EmergencyObject)
        return 'success', 200
    except Exception as e:
        return str(e), 500

@app.route("/ManageVideoStream/postVideoStream", methods=["POST"])
@auth.login_required()
def postVideoStream():
    try:
        jsondata = request.get_json(force=True)
        simpleCoTObject = SendVideoStreamController(jsondata).getCoTObject()
        print("putting in queue")
        APIPipe.put(simpleCoTObject)
        print(simpleCoTObject.xmlString)
        print('put in queue')
        return simpleCoTObject.modelObject.getuid(), 200

    except Exception as e:
        return str(e), 500

"""@app.route("/ManageGeoObject/getGeoObject", methods=[restMethods.GET])
@auth.login_required
def getGeoObject():
    try:
        from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
        return jsonify(list(RestEnumerations().supportedTypeEnumerations.keys()))
    except Exception as e:
        return e, 500"""

@app.route("/ManageChat")
@auth.login_required()
def ManageChat():
    pass

@app.route("/ManageChat/postChatToAll", methods=[restMethods.POST])
@auth.login_required
def postChatToAll():
    try:
        from json import dumps
        #jsondata = {'message': 'test abc', 'sender': 'natha'}
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_chat_post(jsondata)
        ChatObject = SendChatController(jsonobj).getCoTObject()
        APIPipe.put(ChatObject)
        return 'success', 200
    except Exception as e:
        return str(e), 500

@app.route("/ManageEmergency/getEmergency", methods=[restMethods.GET])
@auth.login_required
def getEmergency():
    try:
        output = getemergencys()
        return jsonify(json_list=output), 200
    except Exception as e:
        return str(e), 200

@app.route("/ManageEmergency/postEmergency", methods=[restMethods.POST])
@auth.login_required
def postEmergency():
    try:
        from json import dumps

        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_emergency_post(jsondata)
        EmergencyObject = SendEmergencyController(jsonobj).getCoTObject()
        APIPipe.put(EmergencyObject)
        return EmergencyObject.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 200

@app.route("/ManageEmergency/deleteEmergency", methods=[restMethods.DELETE])
@auth.login_required
def deleteEmergency():
    try:
        from json import dumps
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_emergency_delete(jsondata)
        EmergencyObject = SendEmergencyController(jsonobj).getCoTObject()
        APIPipe.put(EmergencyObject)
        return 'success', 200
    except Exception as e:
        return str(e), 500

@app.route("/Sensor")
@auth.login_required
def sensor():
    pass

@app.route("/Sensor/postDrone", methods=["POST"])
@auth.login_required
def postDroneSensor():
    try:
        from json import dumps

        jsondata = request.get_json(force=True)
        print(jsondata)
        jsonobj = JsonController().serialize_drone_sensor_post(jsondata)
        DroneObject = SendSensorDroneController(jsonobj).getCoTObject()


        print(DroneObject.xmlString)
        APIPipe.put(DroneObject)
        if jsonobj.getSPILongitude() or jsonobj.getSPILatitude() or jsonobj.getSPIName():
            jsonobjSPI = JsonController().serialize_spi_post(jsondata)
            jsonobjSPI.setlatitude(jsonobj.getSPILatitude())
            jsonobjSPI.setlongitude(jsonobj.getSPILongitude())
            jsonobjSPI.setname(jsonobj.getSPIName())
            jsonobjSPI.setdroneUid(DroneObject.modelObject.getuid())
            SPISensor = SendSPISensorController(jsonobjSPI).getCoTObject()
            APIPipe.put(SPISensor)
            return json.dumps({"uid": DroneObject.modelObject.getuid(), "SPI_uid": SPISensor.modelObject.getuid()}), 200
        return DroneObject.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 200

@app.route("/Sensor/postSPI", methods=["POST"])
@auth.login_required
def postSPI():
    try:
        from json import dumps

        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_spi_post(jsondata)
        SPIObject = SendSPISensorController(jsonobj).getCoTObject()
        APIPipe.put(SPIObject)
        return SPIObject.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 200

@app.route("/MapVid", methods=["POST"])
@auth.login_required
def mapvid():
    from json import dumps
    jsondata = request.get_json(force=True)
    jsonobj = JsonController().serialize_imagery_video(jsondata)
    ImagerVideoObject = SendImageryVideoController(jsonobj).getCoTObject()
    APIPipe.put(ImagerVideoObject)
    return 200

@app.route("/AuthenticateUser", methods=["GET"])
@auth.login_required
def authenticate_user():
    try:
        print('request made')
        username = request.args.get("username")
        password = request.args.get("password")
        try:
            user = dbController.query_systemUser(query=(f'name = "{username}"'))[0]
        except Exception as e:
            print(e)
            return None
        if user.password == password:
            print("query made")
            user.metadata = None
            user.query = None
            user.query_class = None
            user._decl_class_registry = None
            user._sa_class_manager = None
            user._sa_instance_state = None
            user._modified_event = None
            print("done setting to none")
            json_user = user.__dict__
            print(json_user)
            del (json_user["_sa_class_manager"])
            del (json_user["_sa_instance_state"])
            del (json_user["_modified_event"])
            del (json_user["_decl_class_registry"])
            print('done defining dict')
            return_data = json.dumps({"uid": json_user["uid"]})
            print('returning data '+str(return_data))
            return return_data
        else:
            return None
    except Exception as e:
        print(e)
        return e, 500

@app.route("/ManageEmergency")
@auth.login_required
def Emergency():
    pass

#@app.route("/ConnectionMessage", methods=[restMethods.POST])
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
        APIPipe.put(object.SendGeoChat)
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
                dbController.remove_APIUser(query=f'Username = "{username}"')
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
            CommandPipe.put([functionNames.Clients])
            out = CommandPipe.get()
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
        import random
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
                dbController.create_Federation(**new_fed, id = id)
                if new_fed["status"] == "Enabled":
                    CommandPipe.put((id, "CREATE"))
                else:
                    pass
            return '', 200

        elif request.method == "PUT":
            jsondata = json.loads(request.data)
            federations = jsondata["federations"]
            for fed in federations:
                old_fed = dbController.query_Federation(f'id = "{fed["id"]}"')[0]
                old_status = old_fed.status
                old_id = old_fed.id
                dbController.update_Federation(column_value=fed, query=f'id = "{fed["id"]}"')
                if "status" in fed:
                    if fed["status"] == "Enabled":

                        if old_status != "Enabled":
                            CommandPipe.put((old_id, "CREATE"))
                        else:
                            pass
                    elif fed["status"] == "Disabled":
                        if old_status != "Disabled":
                            CommandPipe.put((old_id, "DELETE"))
                        else:
                            pass
                    else:
                        pass
            return '', 200

        elif request.method == "DELETE":
            jsondata = json.loads(request.data)
            federations = jsondata["federations"]
            for fed in federations:
                fedInstance = dbController.query_Federation(f'id = "{fed["id"]}"')[0]
                if fedInstance.status == "Enabled":
                    CommandPipe.put((fedInstance.id, "DELETE"))
                else:
                    pass
                dbController.remove_Federation(f'id = "{fed["id"]}"')
            return '', 200

    except Exception as e:
        return str(e), 500

@app.route('/ManageKML/postKML', methods=[restMethods.POST])
@auth.login_required()
def create_kml():
    from pykml.factory import KML_ElementMaker as KML
    from pathlib import Path, PurePath
    from lxml import etree
    import hashlib
    from zipfile import ZipFile
    from lxml.etree import SubElement, Element
    dp_directory = str(PurePath(Path(MainConfig.DataPackageFilePath)))
    jsondata = request.get_json(force=True)
    name = jsondata["name"]
    main = parser.fromstring('<kml xmlns="http://www.opengis.net/kml/2.2"/>')
    root = KML.Document()
    main[0].append(root)
    root[0].append(KML.description(name))
    root[0].append(KML.Folder())
    root.Folder[0].append(KML.Placemark())
    root.Folder.Placemark[0].append(KML.name(name))
    root.Folder.Placemark[0].append(KML.ExtendedData())
    root.Folder.Placemark[0].append(KML.Point(KML.coordinates(str(jsondata["longitude"])+","+str(jsondata["latitude"]))))
    attribs = root.Folder.Placemark.ExtendedData[0]
    for key, value in jsondata["body"].items():
        attribs.append(KML.Data(KML.value(value), name=key))

    # create DP
    tempuid = str(uuid.uuid4())
    app.logger.info(f"Data Package hash = {str(tempuid)}")
    directory = Path(dp_directory, tempuid)
    if not Path.exists(directory):
        os.mkdir(str(directory))
    filepath = str(PurePath(Path(directory), Path(name)))
    data_stringified = etree.tostring(main)
    '''data_stringified = """<?xml version="1.0" encoding="utf-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <description>SALUTE REPORT</description>
    <Folder>
      <Placemark>
        <name>SALUTE REPORT</name>
        <ExtendedData>
          <Data name="title">
            <value>SALUTE REPORT 001</value>
          </Data>
          <Data name="warning" />
          <Data name="userCallsign">
            <value>Corvo</value>
          </Data>
          <Data name="userDescription" />
          <Data name="dateTime">
            <value>2021-05-13T13:55:05.19Z</value>
          </Data>
          <Data name="dateTimeDescription" />
          <Data name="type">
            <value>Surveillance</value>
          </Data>
          <Data name="eventScale">
            <value>Village</value>
          </Data>
          <Data name="scaleDescription" />
          <Data name="importance">
            <value>Routine</value>
          </Data>
          <Data name="status">
            <value>FurtherInvestigation</value>
          </Data>
          <Data name="Time Observed">
            <value>2021-05-13T13:55:05.19Z</value>
          </Data>
          <Data name="Duration of Event">
            <value>All day</value>
          </Data>
          <Data name="Surveillance Type">
            <value>Discreet</value>
          </Data>
          <Data name="Method Of Detection">
            <value>General Observation</value>
          </Data>
          <Data name="Surveillance Mode">
            <value>Vehicle</value>
          </Data>
          <Data name="Location">
            <value>POINT (-77.0104 38.88890079253441)</value>
          </Data>
          <Data name="Range &amp; Bearing to point">
            <value>300:90</value>
          </Data>
          <Data name="Vehicle Type">
            <value>Sedan</value>
          </Data>
          <Data name="Vehicle Color">
            <value>Orange</value>
          </Data>
          <Data name="License Plate" />
          <Data name="Occupants">
            <value>2</value>
          </Data>
          <Data name="Equipment Type">
            <value>Other</value>
          </Data>
          <Data name="Equipment Description">
            <value>UAV</value>
          </Data>
          <Data name="SDR Type">
            <value>Intrusion Points</value>
          </Data>
            <Data name="Assessed Threats">
            <value>Threat to Mission</value>
          </Data>
          <Data name="Final Remarks">
            <value>foo</value>
          </Data>
        </ExtendedData>
        <Point>
          <coordinates>-78.087631247736226,36.46037039687095</coordinates>
        </Point>
      </Placemark>
           </Folder>
  </Document>
</kml>"""'''
    with open(filepath, mode="wb+") as file:

        with ZipFile(file, mode='a') as zip:
            print(zip.infolist())
            uidtemp = uuid.uuid4()
            if "MANIFEST/manifest.xml" not in [member.filename for member in zip.infolist()]:
                manifestXML = Element("MissionPackageManifest", version="2")
                config = SubElement(manifestXML, "Configuration")
                SubElement(config, "Parameter", name="name", value=name)
                SubElement(config, "Parameter", name="uid", value=str(uidtemp))
                zip.writestr(str(uidtemp.hex) + "/" + name + ".kml", data_stringified)
                contents = SubElement(manifestXML, "Contents")
                for fileName in zip.namelist():
                    SubElement(contents, "Content", ignore="false", zipEntry=str(fileName))
                # manifest = zip.open('MANIFEST\\manifest.xml', mode="w")
                zip.writestr('MANIFEST\\manifest.xml', etree.tostring(manifestXML))

                print(zip.namelist())
                file.seek(0)
            else:
                pass

    openfile = open(str(PurePath(Path(str(directory), name))), mode='rb')
    file_hash = str(hashlib.sha256(openfile.read()).hexdigest())
    openfile.close()
    newDirectory = str(PurePath(Path(dp_directory), Path(file_hash)))
    os.rename(str(PurePath(Path(directory))), newDirectory)
    fileSize = Path(str(newDirectory), name).stat().st_size
    uid = str(uuid.uuid4())
    dbController.create_datapackage(uid=uid, Name=name, Hash=file_hash, SubmissionUser='server',
                                    CreatorUid='server-uid', Size=fileSize)

    # broacast DP
    broadcast_datapackage(uid)

    return "successful", 200
@app.route('/BroadcastDataPackage', methods=[restMethods.POST])
@auth.login_required()
def broadcast_datapackage(uid):
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
    DPIP = getStatus().TCPDataPackageService.TCPDataPackageServiceIP
    DPObj = dbController.query_datapackage(f'uid = "{uid}"')[0]
    clientXML = f'<?xml version="1.0"?><event version="2.0" uid="{str(uuid.uuid4())}" type="b-f-t-r" time="{time}" start="{time}" stale="{stale}" how="h-e"><point lat="43.85570300" lon="-66.10801200" hae="19.55866360" ce="3.21600008" le="nan" /><detail><fileshare filename="{DPObj.Name+".zip"}" senderUrl="{DPIP}:8080/Marti/api/sync/metadata/{DPObj.Hash}/tool" sizeInBytes="{DPObj.Size}" sha256="{str(DPObj.Hash)}" senderUid="server-uid" senderCallsign="server" name="{DPObj.Name}" /><ackrequest uid="{uuid.uuid4()}" ackrequested="true" tag="{DPObj.Name}" /></detail></event>'
    cot.xmlString = clientXML.encode()
    newCoT = SendOtherController(cot, addToDB=False)
    APIPipe.put(newCoT.getObject())

@app.route('/DataPackageTable', methods=[restMethods.GET, restMethods.POST, restMethods.DELETE, "PUT"])
@auth.login_required()
def DataPackageTable():
    from pathlib import Path
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
            obj = dbController.query_datapackage(f'Hash = "{Hash}"')
            print(obj)
            # TODO: make this coherent with constants
            currentPath = MainConfig.DataPackageFilePath
            shutil.rmtree(f'{str(currentPath)}/{obj[0].Hash}')
            dbController.remove_datapackage(f'Hash = "{Hash}"')
        return '200', 200

    elif request.method == "POST":
        try:
            import string
            import random
            from pathlib import PurePath, Path
            import hashlib
            from zipfile import ZipFile
            from defusedxml import ElementTree as etree
            import uuid
            from lxml.etree import SubElement, Element
            dp_directory = str(PurePath(Path(MainConfig.DataPackageFilePath)))
            letters = string.ascii_letters
            #uid = ''.join(random.choice(letters) for i in range(4))
            #uid = 'uid-' + str(uid)
            uid = str(uuid.uuid4())
            filename = request.args.get('filename')
            creatorUid = request.args.get('creatorUid')
            file = request.files.getlist('assetfile')[0]
            with ZipFile(file, mode='a') as zip:
                print(zip.infolist())
                if "MANIFEST/manifest.xml" not in [member.filename for member in zip.infolist()]:
                    manifestXML = Element("MissionPackageManifest", version="2")
                    config = SubElement(manifestXML, "Configuration")
                    SubElement(config, "Parameter", name="uid", value=uid)
                    SubElement(config, "Parameter", name="name", value=filename)

                    contents = SubElement(manifestXML, "Contents")
                    for fileName in zip.namelist():
                        SubElement(contents, "Content", ignore="false", zipEntry=str(fileName))
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
            if creatorUid == None:
                callsign = str(dbController.query_user(query=f'uid = "server-uid"', column=[
                    'callsign']))  # fetchone() gives a tuple, so only grab the first element
                dbController.create_datapackage(uid=uid, Name=filename, Hash=file_hash, SubmissionUser='server',
                                                CreatorUid='server-uid', Size=fileSize)
            else:
                callsign = str(dbController.query_user(query=f'uid = f"{creatorUid}"', column=[
                    'callsign']))  # fetchone() gives a tuple, so only grab the first element
                dbController.create_datapackage(uid=uid, Name=filename, Hash=file_hash, SubmissionUser=callsign,
                                                CreatorUid=creatorUid, Size=fileSize)
            return 'successful', 200
        except Exception as e:
            return str(e), 500

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
            dbController.update_datapackage(query=f'PrimaryKey = {dp["PrimaryKey"]}', column_value=updateDict)
        return "success", 200


@app.route("/MissionTable", methods=['GET', 'POST', 'DELETE'])
@auth.login_required()
def mission_table():
    try:
        if request.method == "GET":
            import random

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
        from os import listdir
        from pathlib import PurePath, Path
        from datetime import datetime
        from flask import request
        if request.method == "GET":
            jsondata = {"ExCheck":{'Templates': [], 'Checklists': []}}
            from FreeTAKServer.controllers.ExCheckControllers.templateToJsonSerializer import templateSerializer
            excheckTemplates = DatabaseController().query_ExCheck()
            for template in excheckTemplates:
                templateData = template.data
                templatejson = 	{
                                    "filename": templateData.filename,
                                    "name": templateData.keywords.name,
                                    "submissionTime": templateData.submissionTime,
                                    "submitter": str(dbController.query_user(query=f'uid = "{template.creatorUid}"', column=['callsign'])),
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
                templateitem = DatabaseController().query_ExCheck(f'ExCheckData.uid = "{item["uid"]}"', verbose=True)[0]
                os.remove(str(PurePath(Path(MainConfig.ExCheckFilePath), Path(templateitem.data.filename))))
                DatabaseController().remove_ExCheck(f'PrimaryKey = "{templateitem.PrimaryKey}"')
            for item in ExCheckArray["Checklists"]:
                checklistitem = DatabaseController().query_ExCheckChecklist(f'uid = "{item["uid"]}"')[0]
                os.remove(str(PurePath(Path(MainConfig.ExCheckChecklistFilePath), Path(checklistitem.filename))))
                DatabaseController().remove_ExCheckChecklist(f'uid = "{item["uid"]}"')
            return 'success', 200
        elif request.method == "POST":
            try:
                import uuid
                from FreeTAKServer.controllers.ExCheckControllers.templateToJsonSerializer import templateSerializer
                xmlstring = f'<?xml version="1.0"?><event version="2.0" uid="{uuid.uuid4()}" type="t-x-m-c" time="2020-11-28T17:45:51.000Z" start="2020-11-28T17:45:51.000Z" stale="2020-11-28T17:46:11.000Z" how="h-g-i-g-o"><point lat="0.00000000" lon="0.00000000" hae="0.00000000" ce="9999999" le="9999999" /><detail><mission type="CHANGE" tool="ExCheck" name="exchecktemplates" authorUid="S-1-5-21-2720623347-3037847324-4167270909-1002"><MissionChanges><MissionChange><contentResource><filename>61b01475-ad44-4300-addc-a9474ebf67b0.xml</filename><hash>018cd5786bd6c2e603beef30d6a59987b72944a60de9e11562297c35ebdb7fd6</hash><keywords>test init</keywords><keywords>dessc init</keywords><keywords>FEATHER</keywords><mimeType>application/xml</mimeType><name>61b01475-ad44-4300-addc-a9474ebf67b0</name><size>1522</size><submissionTime>2020-11-28T17:45:47.980Z</submissionTime><submitter>wintak</submitter><tool>ExCheck</tool><uid>61b01475-ad44-4300-addc-a9474ebf67b0</uid></contentResource><creatorUid>S-1-5-21-2720623347-3037847324-4167270909-1002</creatorUid><missionName>exchecktemplates</missionName><timestamp>2020-11-28T17:45:47.983Z</timestamp><type>ADD_CONTENT</type></MissionChange></MissionChanges></mission></detail></event>'
                # this is where the client will post the xmi of a template
                from datetime import datetime
                from defusedxml import ElementTree as etree
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
                APIPipe.put(object)
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
            CommandPipe.put([functionNames.checkStatus])
            FTSServerStatusObject = CommandPipe.get()
            out = ApplyFullJsonController().serialize_model_to_json(FTSServerStatusObject)
            return json.dumps(out), 200
        else:
            return 'endpoint can only be accessed by approved IPs', 401
    except Exception as e:
        return str(e), 500

@app.route('/manageAPI/getHelp', methods=[restMethods.GET])
def help():
    try:
        from flask import url_for
        message = {"APIVersion": "1.7",
                   "SupportedEndpoints": [url_for(i.endpoint, **(i.defaults or {})) for i in app.url_map.iter_rules() if i.endpoint != 'static']
                   }
        return json.dumps(message)
    except Exception as e:
        return e, 500

#@app.route('/changeStatus', methods=[restMethods.POST])
#@auth.login_required()
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
            try:
                FTSObject.CoTService.CoTServicePort = int(CoTService.get(jsonVars.PORT))
            except:
                FTSObject.CoTService.CoTServicePort = ''
            FTSObject.CoTService.CoTServiceStatus = mappings[CoTService.get("status")]
        else:
            pass

        if jsonVars.DATAPACKAGESERVICE in json:

            DPService = json.get(jsonVars.DATAPACKAGESERVICE)
            try:
                FTSObject.TCPDataPackageService.TCPDataPackageServicePort = int(DPService.get(jsonVars.PORT))
            except:
                FTSObject.TCPDataPackageService.TCPDataPackageServicePort = ''
            FTSObject.TCPDataPackageService.TCPDataPackageServiceStatus = mappings[DPService.get("status")]

        else:
            pass

        if jsonVars.SSLDATAPACKAGESERVICE in json:

            DPService = json.get(jsonVars.SSLDATAPACKAGESERVICE)
            try:
                FTSObject.SSLDataPackageService.SSLDataPackageServicePort = int(DPService.get(jsonVars.PORT))
            except:
                FTSObject.SSLDataPackageService.SSLDataPackageServicePort = ''
            FTSObject.SSLDataPackageService.SSLDataPackageServiceStatus = mappings[DPService.get("status")]

        else:
            pass

        if jsonVars.SSLCOTSERVICE in json:

            SSLCoTservice = json[jsonVars.SSLCOTSERVICE]
            try:
                FTSObject.SSLCoTService.SSLCoTServicePort = int(SSLCoTservice.get(jsonVars.PORT))
            except:
                FTSObject.SSLCoTService.SSLCoTServicePort = ''
            FTSObject.SSLCoTService.SSLCoTServiceStatus = mappings[SSLCoTservice.get("status")]

        else:
            pass

        if jsonVars.FEDERATIONSERVERSERVICE in json:

            FederationServerService = json.get(jsonVars.FEDERATIONSERVERSERVICE)
            try:
                FTSObject.FederationServerService.FederationServerServicePort = int(FederationServerService.get(jsonVars.PORT))
            except:
                FTSObject.FederationServerService.FederationServerServicePort = ''
            FTSObject.FederationServerService.FederationServerServiceStatus = mappings[FederationServerService.get('status')]

        else:
            pass

        if jsonVars.RESTAPISERVICE in json:

            RESTAPISERVICE = json.get(jsonVars.RESTAPISERVICE)
            try:
                FTSObject.RestAPIService.RestAPIServicePort = int(RESTAPISERVICE.get(jsonVars.PORT))
            except:
                FTSObject.RestAPIService.RestAPIServicePort = ''
            FTSObject.RestAPIService.RestAPIServiceStatus = mappings[RESTAPISERVICE.get("status")]

        else:
            pass
        FTSObject.SSLDataPackageService.SSLDataPackageServiceIP = ip
        FTSObject.TCPDataPackageService.TCPDataPackageServiceIP = ip
        CommandPipe.put([functionNames.Status, FTSObject])
        out = CommandPipe.get()
        return '200', 200

    except Exception as e:
        return '500', 500

def submitData(dataRaw):
    global APIPipe
    print(APIPipe)
    data = RawCoT()
    data.clientInformation = "SERVER"
    data.xmlString = dataRaw.encode()
    APIPipe.put([data])

def emitUpdates(Updates):
    data = [SimpleClient()]
    data[0].callsign = ''
    data[0].team = ''
    data[0].ip = ''
    returnValue = []
    for client in data:
        returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
    socketio.emit('up', json.dumps(returnValue), broadcast = True)
    data = Updates
    for client in data:
        returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
    socketio.emit('up', json.dumps(returnValue), broadcast = True)
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
    print(etree.tostring(object.sendDropPoint.xmlString,pretty_print=True).decode())
    '''EventObject = json
    modelObject = ApplyFullJsonController(json, 'Point', modelObject).determine_function()
    out = XMLCoTController().serialize_model_to_CoT(modelObject, 'event')
    print(etree.tostring(out))
    print(RestAPI().serializeJsonToModel(modelObject, EventObject))'''



class RestAPI:
    def __init__(self):
        pass

    def startup(self, APIPipea, CommandPipea, IP, Port, starttime):
        print('running api')
        global APIPipe, CommandPipe, StartTime
        StartTime = starttime
        APIPipe = APIPipea
        CommandPipe = CommandPipea
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
