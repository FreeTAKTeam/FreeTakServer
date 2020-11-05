import eventlet
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_httpauth import HTTPTokenAuth
import threading
from lxml import etree
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

functionNames = vars()
functionNames.function_names()

jsonVars = vars()
jsonVars.json_vars()

restMethods = vars()
restMethods.rest_methods()

defaultValues = vars()
defaultValues.default_values()

app = Flask(__name__)
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
    output = dbController.query_APIUser(query=f'token == "{token}"')
    if output:
        return output[0].Username

@app.route('/')
def sessions():
    return b'working'

@socketio.on('connect')
def handle_message():
    emit('data', json.dumps({'abc234': 'test123'}))

@socketio.on('Update')
def handel_updates(msg):
    print(msg)
    emitUpdatesThread = threading.Thread(target=emitUpdates, args=(APIPipe,), daemon=True)
    emitUpdatesThread.start()
    emitUpdatesThread.join()

@app.route("/SendGeoChat", methods=[restMethods.POST])
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
        APIPipe.send(Presence)
        return 'success', 200
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
        from json import dumps
        #jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'attitude': 'friend', 'geoObject': 'Ground', 'how': 'nonCoT', 'name': 'testing123'}
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_geoobject_post(jsondata)
        simpleCoTObject = SendSimpleCoTController(jsonobj).getCoTObject()
        APIPipe.send(simpleCoTObject)
        return 'success', 200
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
        from json import dumps
        #jsondata = {'message': 'test abc', 'sender': 'natha'}
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
        from json import dumps
        output = dbController.query_ActiveEmergency()
        for i in range(0, len(output)):
            output[i] = output[i].__dict__
            del (output[i]['_sa_instance_state'])
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
        APIPipe.send(EmergencyObject)
        return 'success', 200
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
        APIPipe.send(EmergencyObject)
        return 'success', 200
    except Exception as e:
        return str(e), 500

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
        APIPipe.send(object.SendGeoChat)
        return '200', 200
    except Exception as e:
        print(e)

@app.route("/APIUser", methods=[restMethods.GET, restMethods.POST, restMethods.DELETE])
def APIUser():
    if request.remote_addr == 'localhost' or request.remote_addr == '127.0.0.1':
        try:
            if request.method == restMethods.POST:
                json = request.get_json()
                dbController.create_APIUser(Username = json['username'], Token = json['token'])
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
                return jsonify(json_list = output), 200

        except Exception as e:
            return str(e), 500
    else:
        return 'endpoint can only be accessed by localhost', 401
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
        if request.remote_addr == 'localhost' or request.remote_addr == '127.0.0.1':
            CommandPipe.send([functionNames.Clients])
            out = CommandPipe.recv()
            returnValue = []
            for client in out:
                returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
            dumps = json.dumps(returnValue)
            return dumps
        else:
            return 'endpoint can only be accessed by localhost', 401
    except Exception as e:
        return str(e), 500

@app.route('/DataPackageTable', methods=[restMethods.GET, restMethods.POST, "DELETE"])
def DataPackageTable():
    if request.remote_addr == 'localhost' or request.remote_addr == '127.0.0.1':
        if request.method == "GET":
            output = dbController.query_datapackage()
            for i in range(0, len(output)):
                output[i] = output[i].__dict__
                del(output[i]['_sa_instance_state'])
                del(output[i]['CreatorUid'])
                del(output[i]['Hash'])
                del(output[i]['MIMEType'])
                del(output[i]['uid'])
            return jsonify(json_list = output), 200

        elif request.method == "DELETE":
            Hash = request.args.get('Hash')
            obj = dbController.query_datapackage(f'PrimaryKey == "{Hash}"')
            dbController.remove_datapackage(f'PrimaryKey == "{Hash}"')
            # TODO: make this coherent with constants
            currentPath = os.path.dirname(os.path.realpath(__file__))
            shutil.rmtree(f'{str(currentPath)}/FreeTAKServerDataPackageFolder/{obj[0].Hash}')
            return '200', 200
    else:
        return 'endpoint can only be accessed by localhost', 401

@app.route('/checkStatus', methods=[restMethods.GET])
def check_status():
    try:
        if request.remote_addr == 'localhost' or request.remote_addr == '127.0.0.1':
            CommandPipe.send([functionNames.checkStatus])
            FTSServerStatusObject = CommandPipe.recv()
            out = ApplyFullJsonController().serialize_model_to_json(FTSServerStatusObject)
            return json.dumps(out), 200
        else:
            return 'endpoint can only be accessed by localhost', 401
    except Exception as e:
        return str(e), 500

@app.route('/changeStatus', methods=[restMethods.POST])
def All():
    try:
        if request.remote_addr == 'localhost' or request.remote_addr == '127.0.0.1':
            FTSObject = FTS()
            if request.method == restMethods.POST:
                json = request.json
                if jsonVars.COTSERVICE in json:
                    CoTService = json[jsonVars.COTSERVICE]
                    FTSObject.CoTService.CoTServiceIP = CoTService.get(jsonVars.IP)
                    try:
                        FTSObject.CoTService.CoTServicePort = int(CoTService.get(jsonVars.PORT))
                    except:
                        FTSObject.CoTService.CoTServicePort = ''
                    FTSObject.CoTService.CoTServiceStatus = CoTService.get(jsonVars.STATUS)
                else:
                    pass
                if jsonVars.DATAPACKAGESERVICE in json:

                    DPService = json.get(jsonVars.DATAPACKAGESERVICE)
                    FTSObject.TCPDataPackageService.TCPDataPackageServiceIP = DPService.get(jsonVars.IP)
                    try:
                        FTSObject.TCPDataPackageService.TCPDataPackageServicePort = int(DPService.get(jsonVars.PORT))
                    except:
                        FTSObject.TCPDataPackageService.TCPDataPackageServicePort = ''
                    FTSObject.TCPDataPackageService.TCPDataPackageServiceStatus = DPService.get(jsonVars.STATUS)

                else:
                    pass

                CommandPipe.send([functionNames.Status, FTSObject])
                out = CommandPipe.recv()
                return '200', 200
        else:
            return 'endpoint can only be accessed by localhost', 401
    except Exception as e:
        return '500', 500

def receiveUpdates():
    while True:
        try:
            update = APIPipe.recv()
            global UpdateArray
            UpdateArray.append(update)
            print(UpdateArray)
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
    socketio.emit('up', json.dumps(returnValue))
    while True:
        try:
            for _ in UpdateArray:
                returnValue = []
                print(UpdateArray)
                data = UpdateArray.pop(0)
                for client in data:
                    returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
                socketio.emit('up', json.dumps(returnValue))
            socketio.sleep(0.1)
        except Exception as e:
            print(e)
            pass

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

    def startup(self, APIPipea, CommandPipea, IP, Port):
        global APIPipe, CommandPipe
        APIPipe = APIPipea
        CommandPipe = CommandPipea
        threading.Thread(target=receiveUpdates, daemon=True, args=()).start()
        print('rest api starting')
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
    RestAPI().startup()
    #    app.run(host="127.0.0.1", port=80)

