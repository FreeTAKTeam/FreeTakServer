from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
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
import os
import shutil
import json
from flask_cors import CORS

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
app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConfiguration().DataBaseConnectionString
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
dbController.session = db.session
CORS(app)
socketio = SocketIO(app, async_handlers=True, async_mode="threading")
socketio.init_app(app, cors_allowed_origins="*")
APIPipe = None
CommandPipe = None
app.config["SECRET_KEY"] = 'vnkdjnfjknfl1232#'


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

@app.route("/ConnectionMessage", methods=[restMethods.POST])
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
        CommandPipe.send([functionNames.Clients])
        out = CommandPipe.recv()
        returnValue = []
        for client in out:
            returnValue.append(ApplyFullJsonController().serialize_model_to_json(client))
        dumps = json.dumps(returnValue)
        return dumps
    except Exception as e:
        return str(e), 500

@app.route('/DataPackageTable', methods=[restMethods.GET, restMethods.POST, "DELETE"])
def DataPackageTable():
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
                FTSObject.DataPackageService.DataPackageServiceIP = DPService.get(jsonVars.IP)
                try:
                    FTSObject.DataPackageService.DataPackageServicePort = int(DPService.get(jsonVars.PORT))
                except:
                    FTSObject.DataPackageService.DataPackageServicePort = ''
                FTSObject.DataPackageService.DataPackageServiceStatus = DPService.get(jsonVars.STATUS)

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

