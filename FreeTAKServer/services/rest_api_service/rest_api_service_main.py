from flask import Flask, request, jsonify, session, send_file, views
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_httpauth import HTTPTokenAuth
from flask_login import current_user, LoginManager
import threading
from functools import wraps
import uuid
import datetime as dt
import datetime
from defusedxml import ElementTree as etree
import os
import shutil
import json
from flask_cors import CORS
import qrcode
import io
from typing import Dict, List
import time

from digitalpy.core.service_management.digitalpy_service import DigitalPyService
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.request import Request
from digitalpy.core.parsing.formatter import Formatter

from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController

from FreeTAKServer.core.util import certificate_generation
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.RawCoT import RawCoT
from FreeTAKServer.core.parsers.ApplyFullJsonController import ApplyFullJsonController
from FreeTAKServer.core.parsers.XMLCoTController import XMLCoTController
from FreeTAKServer.model.ServiceObjects.FTS import FTS
from FreeTAKServer.core.configuration.RestAPIVariables import RestAPIVariables as vars
from FreeTAKServer.model.SimpleClient import SimpleClient
from FreeTAKServer.core.persistence.DatabaseController import DatabaseController
from FreeTAKServer.core.configuration.DatabaseConfiguration import DatabaseConfiguration
from FreeTAKServer.core.RestMessageControllers.SendChatController import SendChatController
from FreeTAKServer.core.RestMessageControllers.SendDeleteVideoStreamController import \
    SendDeleteVideoStreamController
from FreeTAKServer.core.serializers.xml_serializer import XmlSerializer
from FreeTAKServer.core.RestMessageControllers.SendSimpleCoTController import SendSimpleCoTController, \
    UpdateSimpleCoTController
from FreeTAKServer.core.RestMessageControllers.SendPresenceController import SendPresenceController, \
    UpdatePresenceController
from FreeTAKServer.core.RestMessageControllers.SendEmergencyController import SendEmergencyController
from FreeTAKServer.core.RestMessageControllers.SendSensorDroneController import SendSensorDroneController
from FreeTAKServer.core.RestMessageControllers.SendSPISensorController import SendSPISensorController
from FreeTAKServer.core.RestMessageControllers.SendImageryVideoController import SendImageryVideoController
from FreeTAKServer.core.RestMessageControllers.SendRouteController import SendRouteController
from FreeTAKServer.core.RestMessageControllers.SendVideoStreamController import SendVideoStreamController
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.parsers.JsonController import JsonController
from FreeTAKServer.core.serializers.SqlAlchemyObjectController import SqlAlchemyObjectController
from FreeTAKServer.components.extended.excheck.controllers.ExCheckController import ExCheckController

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
auth = HTTPTokenAuth(scheme='Bearer')
app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConfiguration().DataBaseConnectionString
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
socketio = SocketIO(app, async_handlers=True, async_mode="eventlet")
socketio.init_app(app, cors_allowed_origins="*")
APIPipe = None
CommandPipe = None
config = MainConfig.instance()
app.config["SECRET_KEY"] = config.SecretKey
eventDict = {}

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

loggingConstants = LoggingConstants(log_name="FTS-RestAPI_Service")
logger = CreateLoggerController("FTS-RestAPI_Service", logging_constants=loggingConstants).getLogger()

#TODO Change everything about this
def init_config():
    global dbController

    dbController = DatabaseController()
    dbController.session = db.session


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
                dbController.create_APICall(user_id=output.uid, timestamp=dt.datetime.now(), content=request.data,
                                            endpoint=request.base_url)
                return output.name


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
    emit('connectUpdate', json.dumps({"starttime": str(StartTime), "version": str(config.version)}))


@socketio.on('authenticate')
def authenticate(token):
    if json.loads(token)["Authenticate"] == config.websocketkey:
        emit('authentication', json.dumps({'successful': 'True'}))
        session.authenticated = True  # pylint: disable=assigning-non-slot; this is necessary to save a client's state
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
            except:
                output[i]['callsign'] = "undefined"
                output[i]['team'] = "undefined"
            del (output[i]['_sa_instance_state'])
            del (output[i]['CoT_id'])
            del (output[i]['CoT'])
        except Exception as e:
            logger.error(str(e))
    socketio.emit('userUpdate', json.dumps({"Users": output}))


@socketio.on('logs')
@socket_auth(session=session)
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
            for line in reversed(open(LoggingConstants().ERRORLOG + '.' + str(num), "r").readlines()):
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
    CommandPipe.put([functionNames.checkStatus])
    out = CommandPipe.get()
    while hasattr(out, "CoTService") == False:
        out = CommandPipe.get()
    return out


@socketio.on("serverHealth")
@socket_auth(session=session)
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
    logger.info('systme status running')
    from FreeTAKServer.core.health.ServerStatusController import ServerStatusController
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
    jsondata = get_system_users()

    emit('systemUsersUpdate', json.dumps(jsondata))

@app.route('/ManageSystemUser/getAll', methods=["GET"])
@auth.login_required
def getSystemUsersRest():
    """ wrapper around the updateSystemUser function for Rest API
    """
    try:
        jsondata = get_system_users()
        return json.dumps(jsondata), 200
    except Exception as e:
        logger.error(str(e))
        return "An error occured attempting to retrieve user(s).", 500

def get_system_users():
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
        userjson["DeviceType"] = user.device_type
        jsondata["SystemUsers"].append(userjson)
    return jsondata


@socketio.on('systemUser')
@socket_auth(session=session)
def systemUsers(empty=None):
    jsondata = get_system_users()

    emit('systemUsersUpdate', json.dumps(jsondata))

@app.route('/ManageSystemUser/getSystemUser', methods=["GET"])
@auth.login_required
def getSystemUserRest():
    """ wrapper around the updateSystemUser function for Rest API
    """
    try:
        jsondata = get_system_user(request.json)
        return json.dumps(jsondata), 200
    except Exception as e:
        logger.error(str(e))
        return "An error occured attempting to retrieve user.", 500

def get_system_user(jsondata):
    systemUserArray = DatabaseController().query_by_systemUser(**jsondata)
    jsondata = {"SystemUsers": []}
    for user in systemUserArray:
        userjson = {}
        userjson['Name'] = user.name
        userjson["Group"] = user.group
        userjson["Token"] = user.token
        userjson["Password"] = user.password
        userjson["Certs"] = user.certificate_package_name
        userjson["Uid"] = user.uid
        userjson["DeviceType"] = user.device_type
        jsondata["SystemUsers"].append(userjson)
    return jsondata


@socketio.on('updateSystemUser')
@socket_auth(session=session)
def updateSystemUserWebsocket(jsondata):
    """ wrapper around the updateSystemUser function for websockets
    """
    try:
        return updateSystemUser(json.loads(jsondata))
    except Exception as e:
        logger.error(str(e))
        return "An error occured attempting to update user.", 500

@app.route('/ManageSystemUser/putSystemUser', methods=["PUT"])
@auth.login_required
def updateSystemUserRest():
    """ wrapper around the updateSystemUser function for Rest API
    """
    try:
        updateSystemUser(request.json)
        return 'user updated', 200
    except Exception as e:
        logger.error(str(e))
        return "An error occured attempting to update user.", 500

def updateSystemUser(jsondata):
    """ this function updates an existing system user entry in the database. User id must be provided if user with specified id doesn't
    exist operation will return an error
    Args:
        jsondata: dict
    Returns: None
    """
    for systemuser in jsondata['systemUsers']:
        update_column = {}

        if "Token" in systemuser:
            update_column["token"] = str(systemuser["Token"])
        if "Password" in systemuser:
            update_column["password"] = str(systemuser["Password"])
        if "Group" in systemuser:
            update_column["group"] = str(systemuser["Group"])
        dbController.update_systemUser(query=f'uid = "{systemuser["uid"]}"', column_value=update_column)
    get_system_users()


@socketio.on('addSystemUser')
@socket_auth(session=session)
def addSystemUserWebsocket(jsondata):
    """ wrapper around the addSystemUser function for websockets
    """
    try:
        addSystemUser(json.loads(jsondata))
    except Exception as e:
        logger.error(str(e))
        return "An error occured attempting to add user(s) to the system.", 500

@app.route('/ManageSystemUser/postSystemUser', methods=["POST"])
@auth.login_required
def addSystemUserRest():
    """ wrapper around the addSystemUser function for Rest API
    """
    try:
        return addSystemUser(request.json)
    except Exception as e:
        logger.error(str(e))
        return "An error occured attempting to add user(s) to the system.", 500

def addSystemUser(jsondata):
    """ method which adds new system user
    """
    errors = []
    for systemuser in jsondata['systemUsers']:
        try:
            user_id = str(uuid.uuid4())
            if systemuser["Certs"] == "true":

                # if certs are to be generated the certificate generation is called DP is created and CoT is sent to
                # client resulting in an automatic download of the certificate

                cert_name = systemuser["Name"] + user_id
                # create certs
                certificate_generation.AtakOfTheCerts().bake(common_name=cert_name)
                if systemuser["DeviceType"].lower() == "wintak":
                    certificate_generation.generate_wintak_zip(user_filename=cert_name + '.p12')
                elif systemuser["DeviceType"].lower() == "mobile":
                    certificate_generation.generate_standard_zip(user_filename=cert_name+'.p12')
                else:
                    raise Exception("invalid device type, must be either mobile or wintak")
                # add DP
                import string
                import random
                from pathlib import PurePath, Path
                import hashlib
                from defusedxml import ElementTree as etree
                import shutil
                import os
                dp_directory = str(PurePath(Path(config.DataPackageFilePath)))
                openfile = open(str(PurePath(Path(str(config.ClientPackages), cert_name + '.zip'))),
                                mode='rb')
                file_hash = str(hashlib.sha256(openfile.read()).hexdigest())
                openfile.close()
                newDirectory = str(PurePath(Path(dp_directory), Path(file_hash)))
                os.mkdir(newDirectory)
                shutil.copy(str(PurePath(Path(str(config.ClientPackages), cert_name + '.zip'))),
                            str(PurePath(Path(newDirectory), Path(cert_name + '.zip'))))
                fileSize = Path(str(newDirectory), cert_name + '.zip').stat().st_size
                dbController.create_datapackage(uid=user_id, Name=cert_name + '.zip', Hash=file_hash,
                                                SubmissionUser='server',
                                                CreatorUid='server-uid', Size=fileSize, Privacy=1)
                dbController.create_systemUser(name=systemuser["Name"], group=systemuser["Group"],
                                                token=systemuser["Token"], password=systemuser["Password"],
                                                uid=user_id,
                                                certificate_package_name=cert_name + '.zip', device_type = systemuser["DeviceType"])
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
                from FreeTAKServer.core.SpecificCoTControllers.SendOtherController import SendOtherController
                from FreeTAKServer.model.RawCoT import RawCoT
                cot = RawCoT()
                DPIP = getStatus().TCPDataPackageService.TCPDataPackageServiceIP
                clientXML = f'<?xml version="1.0"?><event version="2.0" uid="{user_id}" type="b-f-t-r" time="{time}" start="{time}" stale="{stale}" how="h-e"><point lat="43.85570300" lon="-66.10801200" hae="19.55866360" ce="3.21600008" le="nan" /><detail><fileshare filename="{cert_name}" senderUrl="{DPIP}:8080/Marti/api/sync/metadata/{str(file_hash)}/tool" sizeInBytes="{fileSize}" sha256="{str(file_hash)}" senderUid="{"server-uid"}" senderCallsign="{"server"}" name="{cert_name + ".zip"}" /><ackrequest uid="{uuid.uuid4()}" ackrequested="true" tag="{cert_name + ".zip"}" /><marti><dest callsign="{systemuser["Name"]}" /></marti></detail></event>'
                cot.xmlString = clientXML.encode()
                newCoT = SendOtherController(cot, addToDB=False)
                APIPipe.put(newCoT.getObject())

            else:
                # in the event no certificate is to be generated simply create a system user
                dbController.create_systemUser(name=systemuser["Name"], group=systemuser["Group"],
                                                token=systemuser["Token"], password=systemuser["Password"],
                                                uid=user_id, device_type = systemuser["DeviceType"])
        except Exception as e:
            logger.error(str(e))
            if isinstance(systemuser, dict) and "Name" in systemuser:
                errors.append(f"operation failed for user {systemuser['Name']}")
            else:
                errors.append(f"operation failed for user. missing name parameter.")

    if len(errors) == 0:
        return "all users created", 201
    elif len(errors)<len(jsondata['systemUsers']):
        return ", ".join(errors), 201
    else:
        return "all users failed to create "+", ".join(errors), 500

@socketio.on("removeSystemUser")
@socket_auth(session=session)
def removeSystemUserWebsocket(jsondata):
    """ wrapper around the removeSystemUser function for websockets
    """
    try:
        removeSystemUser(json.loads(jsondata))
    except Exception as e:
        logger.error(str(e))
        return "An error occured attempting to remove the user(s).", 500

@app.route('/ManageSystemUser/deleteSystemUser', methods=["DELETE"])
@auth.login_required
def removeSystemUserRest():
    """ wrapper around the removeSystemUser function for Rest API
    """
    try:
        removeSystemUser(request.json)
        return 'user deleted', 200
    except Exception as e:
        logger.error(str(e))
        return "An error occured attempting to remove the user(s).", 500

def removeSystemUser(jsondata):
    """ iterates through a list of system users and removes them in addition to revoking and
    deleting their certificates.
    """
    from FreeTAKServer.core.util.certificate_generation import revoke_certificate
    for systemUser in jsondata["systemUsers"]:
        uid = systemUser["uid"]
        systemUser = dbController.query_systemUser(query=f'uid = "{uid}"')[0]
        na = systemUser.name
        revoke_certificate(username=na+uid)
        certificate_package_name = systemUser.certificate_package_name
        dbController.remove_systemUser(f'uid = "{uid}"')
        obj = dbController.query_datapackage(f'Name = "{certificate_package_name}"')
        # TODO: make this coherent with constants
        currentPath = config.DataPackageFilePath
        shutil.rmtree(f'{str(currentPath)}/{obj[0].Hash}')
        dbController.remove_datapackage(f'Hash = "{obj[0].Hash}"')
        os.remove(config.certsPath + f"/{na}{uid}.pem")
        os.remove(config.certsPath + f"/{na}{uid}.key")
        os.remove(config.certsPath + f"/{na}{uid}.p12")
    return '', 200

@socketio.on("events")
@socket_auth(session=session)
def events(empty=None):
    current_notifications = Notification()
    # socketio.emit(json.dumps([current_notifications.logErrors, current_notifications.emergencys]))
    emit("eventsUpdate", {"events": current_notifications.logErrors + current_notifications.emergencys})

@app.route('/GenerateQR', methods=["GET"])
def generate_qr():
    datapackage_id = request.args.get('datapackage_id')
    dp = dbController.query_datapackage(query=f"PrimaryKey={datapackage_id}")[0]
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    qr.add_data(f'http://{config.DataPackageServiceDefaultIP}:{8080}/Marti/api/sync/metadata/{dp.Hash}/tool')
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/ManageNotification/getNotification', methods=["GET"])
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
            if len(line_segments) > 4:
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
            output[i]["remarks"] = original.event.detail.remarks.INTAG
            del (output[i]['_sa_instance_state'])
            del (output[i]['event'])
        except:
            pass
    return output


class Notification:
    def __init__(self):
        try:
            self.emergencys = [i["name"] + " " + i["type"] for i in getemergencys()]
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
        from FreeTAKServer.core.SpecificCoTControllers.SendGeoChatController import SendGeoChatController
        rawcot = RawCoT()
        rawcot.xmlString = xml
        rawcot.clientInformation = None
        object = SendGeoChatController(rawcot)
        APIPipe.put(object.getObject())
        return '200', 200
    except Exception as e:
        logger.error(str(e))


@app.route("/ManagePresence")
@auth.login_required()
def ManagePresence():
    pass


@app.route("/ManagePresence/postPresence", methods=[restMethods.POST])
@auth.login_required
def postPresence():
    try:
        from json import dumps
        # jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'how': 'nonCoT', 'name': 'testing123'}
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_presence_post(jsondata)
        Presence = SendPresenceController(jsonobj).getCoTObject()
        APIPipe.put(Presence)
        return Presence.modelObject.getuid(), 200
    except Exception as e:
        logger.error(str(e))
        return "An error occurred managing presence.", 500


@app.route("/ManagePresence/putPresence", methods=["PUT"])
@auth.login_required
def putPresence():
    try:
        from json import dumps
        # jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'how': 'nonCoT', 'name': 'testing123'}
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_presence_post(jsondata)
        Presence = UpdatePresenceController(jsonobj).getCoTObject()
        APIPipe.put(Presence)
        return Presence.modelObject.getuid(), 200
    except Exception as e:
        logger.error(str(e))
        return "An error occurred managing presence.", 500


@app.route("/ManageRoute")
@auth.login_required()
def ManageRoute():
    pass


@app.route("/ManageRoute/postRoute", methods=["POST"])
@auth.login_required()
def postRoute():
    try:
        from json import dumps
        # jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'how': 'nonCoT', 'name': 'testing123'}
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_route_post(jsondata)
        Route = SendRouteController(jsonobj).getCoTObject()
        APIPipe.put(Route)
        return Route.modelObject.getuid(), 200
    except Exception as e:
        logger.error(str(e))
        return "An error occurred managing route.", 500


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
        radius_in_deg = (geopy.units.degrees(arcseconds=geopy.units.nautical(meters=radius))) / 2

        results = dbController.query_CoT(query=[Event.point.has(or_(and_(Point.lon < 0, Point.lat < 0, (
                    (((Point.lon * -1) - lon_abs) * 111302.62) + (
                        ((Point.lat * -1) - lat_abs) * 110574.61)) <= radius + 10), and_(Point.lon < 0, Point.lat >= 0,
                                                                                         ((((
                                                                                                        Point.lon * -1) - lon_abs) * 111302.62) + (
                                                                                                      (
                                                                                                                  Point.lat - lat_abs) * 110574.61)) <= radius + 10),
                                                                    and_(Point.lon >= 0, Point.lat < 0, (
                                                                                ((Point.lon - lon_abs) * 111302.62) + ((
                                                                                                                                   (
                                                                                                                                               Point.lat * -1) - lat_abs) * 110574.61)) <= radius + 10),
                                                                    and_(Point.lon >= 0, Point.lat >= 0, (
                                                                                ((Point.lon - lon_abs) * 111302.62) + ((
                                                                                                                                   Point.lat - lat_abs) * 110574.61)) <= radius + 10)))])
        print(results)
        output = []
        for result in results:
            try:
                dLon = (result.point.lon - lon)
                x = cos(radians(result.point.lat)) * sin(radians(dLon))
                y = cos(radians(lat)) * sin(radians(result.point.lat)) - sin(radians(lat)) * cos(
                    radians(result.point.lat)) * cos(radians(dLon))
                brng = atan2(x, y)
                brng = degrees(brng)
                type_pattern = [type for type in list(RestEnumerations.supportedTypeEnumerations.values()) if
                                re.fullmatch(type, result.type)][0]
                index_number = list(RestEnumerations.supportedTypeEnumerations.values()).index(type_pattern)
                type = list(RestEnumerations.supportedTypeEnumerations.keys())[index_number]
                print(type)
                part1 = result.type.split(type_pattern.split('.')[0])
                part2 = '-' + part1[1].split(type_pattern.split('.')[1])[0] + '-'
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
        logger.error(str(e))
        return "An error occurred retrieving zone CoT.", 500



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
        radius = request.args.get("radius", default=100, type=int)
        lat = request.args.get("latitude", default=0, type=float)
        lon = request.args.get("longitude", default=0, type=float)
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
            results = dbController.query_CoT(query=Event.point.has(and_(
                Point.lon >= 0,
                Point.lat >= 0,
                or_(
                    and_(
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) <= radius + 10,
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) >= 0),
                    and_((
                        ((lon_abs - Point.lon) * 111302.62) + ((lon_abs - Point.lat) * 110574.61)) <= radius + 10,
                        (((lon_abs - Point.lon) * 111302.62) + ((lon_abs - Point.lat) * 110574.61)) >= 0)))))
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
            results = dbController.query_CoT(query=Event.point.has(and_(
                Point.lon < 0,
                Point.lat >= 0,
                or_(
                    and_(
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) <= radius + 10,
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) > 0),
                    and_(
                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) <= radius + 10,
                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) > 0)
                ))))

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
                logger.error(str(e))
        return json.dumps(output)

    except Exception as e:
        logger.error(str(e))
        return "An error occurred retrieving geo object.", 500


#@app.route("/ManageGeoObject/postGeoObject", methods=[restMethods.POST])
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
        logger.error(str(e))
        return "An error occurred adding geo object.", 500


@app.route("/ManageGeoObject/putGeoObject", methods=["PUT"])
@auth.login_required
def putGeoObject():
    try:
        from json import dumps
        # jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'attitude': 'friend', 'geoObject': 'Ground', 'how': 'nonCoT', 'name': 'testing123'}
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
        logger.error(str(e))
        return "An error occurred updating geo object.", 500


@app.route("/ManageVideoStream")
@auth.login_required()
def ManageVideoStream():
    pass


@app.route("/ManageVideoStream/getVideoStream", methods=[restMethods.GET])
@auth.login_required
def getVideoStream():
    try:

        # changed below line to access _Video table directly instead of using full stack call
        # to make this endpoint more robust as well as prevent issues where post does not create
        # full stack entries

        # changed the main return from a list to an object to facilitate further development
        from json import dumps
        from urllib import parse
        from FreeTAKServer.model.SQLAlchemy.CoTTables.Sensor import Sensor

        output = dbController.query_video()
        return_value = {"video_stream": {}}
        for value in output:
            value_obj = return_value["video_stream"][str(value.PrimaryKey)] = {}
            if value.url:
                value_obj["url"] = parse.urlparse(value.url).path
            if value.ConnectionEntry:
                if value.ConnectionEntry.path:
                    value_obj["path"] = value.ConnectionEntry.path
                if value.ConnectionEntry.port:
                    value_obj["port"] = value.ConnectionEntry.port
                if value.ConnectionEntry.address:
                    value_obj["address"] = value.ConnectionEntry.address
        return dumps(return_value), 200
    except Exception as e:
        logger.error(str(e))
        return "An error occurred retrieving video stream.", 500


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
        logger.error(str(e))
        return "An error occurred deleting video stream.", 500


@app.route("/ManageVideoStream/postVideoStream", methods=["POST"])
@auth.login_required()
def postVideoStream():
    """this method contains the logic for the endpoints which saves the contents of a new videostream to
    the db and sends a CoT to all connected clients containing stream information."""
    from FreeTAKServer.model.FTSModel.Event import Event
    from lxml.etree import tostring  # pylint: disable=no-name-in-module; name is in module
    try:
        jsondata = request.get_json(force=True)

        # the following prevents duplicate entries being added to the db
        url = jsondata["streamAddress"] + ":" + jsondata["streamPort"] + jsondata["streamPath"]
        video_streams = dbController.query_videostream()

        for video in video_streams:
            if video.url == url:
                sqlalchemy_obj = dbController.query_CoT(f'uid="{video.PrimaryKey}"')[0]
                modelObject = SqlAlchemyObjectController().convert_sqlalchemy_to_modelobject(sqlalchemy_obj,
                                                                                             Event.VideoStream())
                xmlString = tostring(XmlSerializer().from_fts_object_to_format(modelObject))
                modelObject.xmlString = xmlString
                APIPipe.put(modelObject)
                return "entry already exists in db " + str(video.PrimaryKey) + " resending existing entry", 201

        simpleCoTObject = SendVideoStreamController(jsondata).getCoTObject()
        print("putting in queue")
        APIPipe.put(simpleCoTObject)
        print(simpleCoTObject.xmlString)
        print('put in queue')
        return simpleCoTObject.modelObject.getuid(), 200

    except Exception as e:
        logger.error(str(e))
        return "An error occurred adding video stream.", 500


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
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_chat_post(jsondata)
        ChatObject = SendChatController(jsonobj).getCoTObject()
        APIPipe.put(ChatObject)
        return 'success', 200
    except Exception as e:
        logger.error(str(e))
        return "An error occurred sending chat.", 500

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
        logger.error(str(e))
        return "An error occurred adding drone sensor.", 500


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
        logger.error(str(e))
        return "An error occurred adding SPI details.", 500


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
            logger.error(str(e))
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
            print('returning data ' + str(return_data))
            return return_data
        else:
            return None
    except Exception as e:
        logger.error(str(e))
        return "An error occurred authenticating user.", 500

# @app.route("/ConnectionMessage", methods=[restMethods.POST])
def ConnectionMessage():
    """this endpoint is responsible for generating the CoT equivalen to the content of the JSON sent
    and then forwarding this CoT to all connected clients"""
    try:
        json = request.json
        modelObject = Event.GeoChat()
        out = ApplyFullJsonController().serializeJsonToModel(modelObject, json)
        xml = XMLCoTController().serialize_model_to_CoT(out, 'event')
        from FreeTAKServer.core.RestMessageControllers.SendChatController import SendChatController
        rawcot = RawCoT()
        rawcot.xmlString = xml
        rawcot.clientInformation = None
        object = SendChatController(rawcot).getCoTObject()
        object.type = "connmessage"
        APIPipe.put(object.SendGeoChat)
        return '200', 200
    except Exception as e:
        logger.error(str(e))


@app.route("/APIUser", methods=[restMethods.GET, restMethods.POST, restMethods.DELETE])
def APIUser():
    if request.remote_addr in config.AllowedCLIIPs:
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
            logger.error(str(e))
            return "An error occurred updating api user record.", 500
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
        if request.remote_addr in config.AllowedCLIIPs:
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
        logger.error(str(e))
        return "An error occurred retrieving client details.", 500


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
                dbController.create_Federation(**new_fed, id=id)
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
        logger.error(str(e))
        return "An error occurred accessing federation details.", 500


@app.route('/ManageKML/postKML', methods=[restMethods.POST])
@auth.login_required()
def create_kml():
    # Make a connection to the MainConfig object
    config = MainConfig.instance()

    try:
        from pykml.factory import KML_ElementMaker as KML
        from pykml import parser
        from pathlib import Path, PurePath
        from lxml import etree
        import hashlib
        from zipfile import ZipFile
        from lxml.etree import SubElement, Element  # pylint: disable=no-name-in-module
        from geopy import Nominatim
        dp_directory = str(PurePath(Path(config.DataPackageFilePath)))
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
        if jsondata.get("longitude") and jsondata.get("latitude"):
            root.Folder.Placemark[0].append(
                KML.Point(KML.coordinates(str(jsondata["longitude"]) + "," + str(jsondata["latitude"]))))
        elif jsondata.get("address"):
            locator = Nominatim(user_agent=str(uuid.uuid4()))
            location = locator.geocode(jsondata.get("address"))
            root.Folder.Placemark[0].append(
                KML.Point(KML.coordinates(str(location.longitude) + "," + str(location.latitude))))
        else:
            root.Folder.Placemark[0].append(
                KML.Point(KML.coordinates(str(0) + "," + str(0))))
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
    except Exception as e:
        logger.error(str(e))


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
    from FreeTAKServer.core.SpecificCoTControllers.SendOtherController import SendOtherController
    from FreeTAKServer.model.RawCoT import RawCoT
    cot = RawCoT()
    DPIP = getStatus().TCPDataPackageService.TCPDataPackageServiceIP
    DPObj = dbController.query_datapackage(f'uid = "{uid}"')[0]
    clientXML = f'<?xml version="1.0"?><event version="2.0" uid="{str(uuid.uuid4())}" type="b-f-t-r" time="{time}" start="{time}" stale="{stale}" how="h-e"><point lat="43.85570300" lon="-66.10801200" hae="19.55866360" ce="3.21600008" le="nan" /><detail><fileshare filename="{DPObj.Name + ".zip"}" senderUrl="{DPIP}:8080/Marti/api/sync/metadata/{DPObj.Hash}/tool" sizeInBytes="{DPObj.Size}" sha256="{str(DPObj.Hash)}" senderUid="server-uid" senderCallsign="server" name="{DPObj.Name}" /><ackrequest uid="{uuid.uuid4()}" ackrequested="true" tag="{DPObj.Name}" /></detail></event>'
    cot.xmlString = clientXML.encode()
    newCoT = SendOtherController(cot, addToDB=False)
    APIPipe.put(newCoT.getObject())


@app.route('/DataPackageTable', methods=[restMethods.GET, restMethods.POST, restMethods.DELETE, "PUT"])
@auth.login_required()
def DataPackageTable():
    from pathlib import Path

    # Make a connection to the MainConfig object
    config = MainConfig.instance()

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
            currentPath = config.DataPackageFilePath
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
            from lxml.etree import SubElement, Element  # pylint: disable=no-name-in-module
            dp_directory = str(PurePath(Path(config.DataPackageFilePath)))
            letters = string.ascii_letters
            # uid = ''.join(random.choice(letters) for i in range(4))
            # uid = 'uid-' + str(uid)
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
            logger.error(str(e))
            return "An error occurred accessing datapackage details.", 500

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
        logger.error(str(e))
        return "An error occurred accessing mission details.", 500


@app.route("/ExCheckTable", methods=["GET", "POST", "DELETE"])
@auth.login_required()
def excheck_table():
    return ExCheckController().excheck_table(request, APIPipe)


@app.route('/checkStatus', methods=[restMethods.GET])
@auth.login_required()
def check_status():
    try:

        if request.remote_addr in config.AllowedCLIIPs:
            CommandPipe.put([functionNames.checkStatus])
            FTSServerStatusObject = CommandPipe.get()
            out = ApplyFullJsonController().serialize_model_to_json(FTSServerStatusObject)
            return json.dumps(out), 200
        else:
            return 'endpoint can only be accessed by approved IPs', 401
    except Exception as e:
        logger.error(str(e))
        return "An error occurred accessing server status details.", 500


@app.route('/manageAPI/getHelp', methods=[restMethods.GET])
def help():
    try:
        from flask import url_for
        message = {"APIVersion": str(config.APIVersion),
                   "SupportedEndpoints": [url_for(i.endpoint, **(i.defaults or {})) for i in app.url_map.iter_rules() if
                                          i.endpoint != 'static']
                   }
        return json.dumps(message)
    except Exception as e:
        logger.error(str(e))
        return "An error occurred accessing helper details.", 500


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
                FTSObject.FederationServerService.FederationServerServicePort = int(
                    FederationServerService.get(jsonVars.PORT))
            except:
                FTSObject.FederationServerService.FederationServerServicePort = ''
            FTSObject.FederationServerService.FederationServerServiceStatus = mappings[
                FederationServerService.get('status')]

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
    socketio.emit('up', json.dumps(returnValue), broadcast=True)
    data = Updates
    for client in data:
        returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
    socketio.emit('up', json.dumps(returnValue), broadcast=True)
    return 1

@app.route('/v2/<context>/<action>', methods=[restMethods.GET, restMethods.POST])
@auth.login_required
def api_routing(context, action):
    """the main method for the routing based API which uses information fro
    the route and the method to send the request to the internal router, 
    returning the response

    Args:
        context (str): the context of the request, for use in the routing
        action (str): the action of the request, for use in the routing

    Raises:
        ValueError: if the synchronous parameter is true and the service_idis 

    Returns:
        dict: the values of the response returned by the component
    """
    synchronous = request.args.get("synchronous", True) # all requests are by default synchronous
    service_id = request.args.get("service_id")
    values = request.get_json()
    rest_api_service = ObjectFactory.get_instance("RestAPIService")
    service_id_different = service_id is not None and rest_api_service.service_id != service_id
    if synchronous == True and service_id_different:
        raise ValueError("synchronous is true and service_id is neither None or rest api service id,\
                            this will result in an undefined state where we are waiting for a response that will never come")

    # request to get repeated messages
    internal_request: Request = ObjectFactory.get_new_instance("request")
    internal_request.set_action(action)
    internal_request.set_context(context)
    internal_request.set_sender(rest_api_service.__class__.__name__.lower())
    internal_request.set_format("pickled")
    internal_request.set_values(values or {})
    rest_api_service.subject_send_request(internal_request, APPLICATION_PROTOCOL, service_id)
    if synchronous == True:
        response = rest_api_service.retrieve_response(internal_request.get_id())
        return response.get_values()

# TODO: move this out of the rest_api_service and into it's own file in views
# this will require changing it from using the API Pipe to use the ZManager instead
import json
import datetime as dt
import datetime

from flask import request
from typing import Dict, List
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.request import Request
from geopy import Point, distance

from FreeTAKServer.core.RestMessageControllers.SendSimpleCoTController import SendSimpleCoTController
from FreeTAKServer.core.parsers.JsonController import JsonController

from FreeTAKServer.services.rest_api_service.views.base_view import BaseView
from FreeTAKServer.services.rest_api_service.views.emergency_view import ManageEmergency

class ManageGeoObjects(BaseView):
    """this class is responsible for creating the flask views required for managing
    geo objects in FTS
    """
    decorators = [auth.login_required]
    
    def __init__(self, *args, **kwargs) -> None:
        endpoints: Dict[str, callable] = {
            "GetRepeatedMessages": self.get_repeated_messages,
            "postGeoObject": self.post_geo_object,
            "DeleteRepeatedMessages": self.delete_repeated_messages,
        }
        super().__init__(endpoints)

    def get_repeated_messages(self):
        """method to retrieve a repeated messages
        Returns:
            str: example of json output {"messages": {"example-oid": <event><detail/><point/></event>}}
        """
        try:
            response = self.make_request("GetRepeatedMessages")
            message_nodes = response.get_value("message")

            # request to serialize repeated messages to CoT
            # TODO: parameterize message protocol
            response = self.make_request("serialize", {"message": message_nodes, "protocol": "XML"})

            # convert response to json
            # TODO: this conversion should be automated 
            output = {"messages": {}}
            message = response.get_value("message")
            for i in range(len(message)):
                output["messages"][str(message_nodes[i].uid)] = message[i].decode()
            
            return json.dumps(output)

        except Exception as e:
            return str(e), 500

    def post_geo_object(self):
        """this method is responsible for creating publishing and saving a geoobject to the repeater
        Returns:
            str: the uid of the generated object
        """
        try:
            # jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'attitude': 'friend', 'geoObject': 'Ground', 'how': 'nonCoT', 'name': 'testing123'}
            jsondata = request.get_json(force=True)
            # conver the json body to an object
            jsonobj = JsonController().serialize_geoobject_post(jsondata)
            
            # check if the message it expected to be repeated
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
            # make request to create a geoobject node
            response = self.make_request("CreateGeoObject", {"id": jsonobj.getuid()})
            # apply the given values to the model object
            model_object = response.get_value("model_object")
            model_object.uid = jsonobj.getuid()
            COTTYPE = jsonobj.getgeoObject()
            if "-.-" in COTTYPE:
                ID = jsonobj.getattitude()
                COTTYPE = COTTYPE.replace('-.-', ID)
            else:
                pass
            model_object.type = COTTYPE
            model_object.how = jsonobj.gethow()
            
            model_object.start = None # set to default val
            model_object.time = None  # set to default val
            if jsonobj.gettimeout() != '' and jsonobj.gettimeout() != None:
                DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
                timer = dt.datetime
                now = timer.utcnow()
                add = datetime.timedelta(seconds=int(jsonobj.gettimeout()))
                stale = now+add
                model_object.stale = stale.strftime(DATETIME_FMT)
            else:
                model_object.stale = None # set to default val
            #    DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
            #    timer = dt.datetime
            #    now = timer.utcnow()
            #    zulu = now.strftime(DATETIME_FMT)
            #    add = datetime.timedelta(seconds=int(jsonobj.gettimeout()))
            #    stale_part = dt.datetime.strptime(zulu, DATETIME_FMT) + add
            #model_object.stale = stale_part
            model_object.point.lat = jsonobj.getlatitude()
            model_object.point.lon = jsonobj.getlongitude()
            model_object.detail.contact.callsign = jsonobj.getname()

            # if the message should be repeated then make a request to repeat it
            if jsonobj.getrepeat():
               
                # make request to persist the model object to be re-sent
                response = self.make_request("CreateRepeatedMessage", {"message": [model_object]})

            print("putting in queue")
            APIPipe.put(simpleCoTObject)
            print(simpleCoTObject.xmlString)
            print('put in queue')
            return simpleCoTObject.modelObject.getuid(), 200
        except Exception as e:
            logger.error(str(e))
            return "An error occurred adding geo object.", 500
    
    def delete_repeated_messages(self):
        """delete an existing repeated message
        Returns:
            str: whether or not the operation was sucessful
        """
        try:
            # get and blowup id list
            ids: List[str] = request.args.get("ids").split(",")
            response = self.make_request("DeleteRepeatedMessage", {"ids": ids})
            if response.get_value("success"):
                delete_objs = []  
                for id in ids:
                    # TODO move strings out to constants
                    response = self.make_request("DeleteGeoObject", {"uid": id})
                    model_obj = response.get_value("model_object")
                    model_obj.detail.link.uid = id
                    model_obj.type = "t-x-d-d"
                    model_obj.uid = id
                    model_obj.how = "h-g"
                    model_obj.start = None # set to default val
                    model_obj.time = None  # set to default val
                    model_obj.stale = None # set to default val
                    delete_objs.append(model_obj)
                self.make_request("publish", {"recipients": "*", "message": delete_objs}, False)
                return 'operation successful', 200
            else:
                return 'operation failed', 500
        except Exception as e:
            return str(e), 500

# TODO: move this out of the rest_api_service and into it's own file in views
# this will require changing it from using the API Pipe to use the ZManager instead

ManageEmergency.decorators.append(auth.login_required)
app.add_url_rule('/ManageEmergency/<method>', view_func=ManageEmergency.as_view('/ManageEmergency/<method>'), methods=["POST", "GET","DELETE"])
app.add_url_rule('/ManageGeoObject/<method>', view_func=ManageGeoObjects.as_view('/ManageGeoObject/<method>'), methods=["POST", "GET","DELETE"])

APPLICATION_PROTOCOL = "xml"
API_REQUEST_TIMEOUT = 5000

class RestAPI(DigitalPyService):
    
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

    def stop(self):
        super().stop()
        socketio.stop()

    def start(self, APIPipea, CommandPipea, IP, Port, starttime, factory):
        print('running api')
        super().start()
        self.initialize_connections(APPLICATION_PROTOCOL)
        ObjectFactory.configure(factory)
        init_config()
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