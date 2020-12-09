from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import threading
from lxml import etree
from FreeTAKServer.controllers.model.Event import Event
from FreeTAKServer.controllers.model.RawCoT import RawCoT
from FreeTAKServer.controllers.ApplyFullJsonController import ApplyFullJsonController
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.controllers.model.FTS import FTS
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables as vars
import time
from FreeTAKServer.controllers.model.SimpleClient import SimpleClient

import datetime as dt
import json
from flask_cors import CORS

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
CORS(app)
socketio = SocketIO(app, async_handlers=True, async_mode="threading")
socketio.init_app(app, cors_allowed_origins="*")
APIPipe = None
CommandPipe = None
app.config["SECRET_KEY"] = 'vnkdjnfjknfl1232#'

def receiveUpdates():
    while True:
        try:
            update = UpdatePipe.recv()
            global UpdateArray
            UpdateArray.append(update)
            print(UpdateArray)
        except Exception as e:
            print(e)
@app.route('/')
def sessions():
    return b'working'

@socketio.on('connect')
def handle_message():
    emit('data', json.dumps({'abc234': 'test123'}))

@socketio.on('Update')
def handel_updates(msg):
    print(msg)
    threading.Thread(target=emitUpdates, args=(UpdatePipe,), daemon=True).start()
    time.sleep(100)

@app.route("/SendGeoChat", methods=[restMethods.POST])
def SendGeoChat():
    try:
        json = request.json
        modelObject = Event.GeoChat()
        out = ApplyFullJsonController().serializeJsonToModel(modelObject, json)
        xml = XMLCoTController().serialize_model_to_CoT(out, 'event')
        from FreeTAKServer.controllers.SendGeoChatController import SendGeoChatController
        rawcot = RawCoT()
        rawcot.xmlString = xml
        rawcot.clientInformation = None
        object = SendGeoChatController(rawcot)
        APIPipe.send(object.SendGeoChat)
        return '200', 200
    except Exception as e:
        print(e)
@app.route("/RecentCoT", methods=[restMethods.GET])
def RecentCoT():
    return b'1234'

@app.route("/URL", methods=[restMethods.GET])
def URLGET():
    data = request.args
    print(data)
    return 'completed', 200

@app.route("/Clients", methods=[restMethods.GET])
def Clients():
    try:
        CommandPipe.send([functionNames.Clients])
        out = CommandPipe.recv()
        returnValue = []
        for client in out:
            returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
        print(json.dumps(returnValue))
        return json.dumps(returnValue)
    except Exception as e:
        return str(e), 500

@app.route('/checkStatus', methods=[restMethods.GET])
def check_status():
    try:
        CommandPipe.send([functionNames.checkStatus])
        FTSServerStatusObject = CommandPipe.recv()
        out = ApplyFullJsonController().serialize_model_to_json(FTSServerStatusObject)
        return json.dumps(out), 200
    except Exception as e:
        return str(e), 500

@app.route('/changeStatus', methods=[restMethods.POST])
def All():
    try:
        FTSObject = FTS()
        if request.method == restMethods.POST:
            json = request.json
            CoTService = json[jsonVars.COTSERVICE]
            FTSObject.CoTService.CoTServiceIP = CoTService.get(jsonVars.IP)
            try:
                FTSObject.CoTService.CoTServicePort = int(CoTService.get(jsonVars.PORT))
            except:
                FTSObject.CoTService.CoTServicePort = ''
            FTSObject.CoTService.CoTServiceStatus = CoTService.get(jsonVars.STATUS)
            DPService = json.get(jsonVars.DATAPACKAGESERVICE)
            FTSObject.DataPackageService.DataPackageServiceIP = DPService.get(jsonVars.IP)
            try:
                FTSObject.DataPackageService.DataPackageServicePort = int(DPService.get(jsonVars.PORT))
            except:
                FTSObject.DataPackageService.DataPackageServicePort = ''
            FTSObject.DataPackageService.DataPackageServiceStatus = DPService.get(jsonVars.STATUS)
            CommandPipe.send([functionNames.Status, FTSObject])
            out = CommandPipe.recv()
            return '200', 200

    except Exception as e:
        return '500', 500

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
    from FreeTAKServer.controllers.SendDropPointController import SendDropPointController
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

    def startup(self, APIPipea, CommandPipea, updates, IP, Port):
        global APIPipe, CommandPipe, UpdatePipe
        APIPipe = APIPipea
        CommandPipe = CommandPipea
        UpdatePipe = updates
        threading.Thread(target=receiveUpdates, daemon=True).start()
        socketio.run(app, host=IP, port=Port, debug=True, use_reloader=False)

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

