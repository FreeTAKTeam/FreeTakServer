from FreeTAKServer.model.RestMessages.Emergency import Emergency as Obj
from FreeTAKServer.controllers.RestMessageControllers.SendChatController import SendChatController
from FreeTAKServer.controllers.RestMessageControllers.SendPresenceController import SendPresenceController
from FreeTAKServer.controllers.RestMessageControllers.SendEmergencyController import SendEmergencyController
from FreeTAKServer.controllers.RestMessageControllers.SendSimpleCoTController import SendSimpleCoTController
from flask import Flask, request, jsonify
from FreeTAKServer.controllers.JsonController import JsonController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables as vars
from flask_httpauth import HTTPTokenAuth

dbController = DatabaseController()
restMethods = vars()
restMethods.rest_methods()
app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')


class GeoObject:

    @staticmethod
    def create_geoobject(json_data: dict) -> object:
        """
        create a geoobject FTSModel Object From information specified in supplied JSON argument

        @param json_data:
        @return:
        """
        jsonobj = JsonController().serialize_geoobject_post(json_data)
        simpleCoTObject = SendSimpleCoTController(jsonobj).getCoTObject()
        return simpleCoTObject


class Presence:

    @staticmethod
    def create_presence(jsondata: dict) -> object:
        """
        create a presence FTSModel Object from information specified in supplied Json argument

        @type: object
        @param jsondata:
        @return Event:
        @raise Exception:
        """
        try:
            json_obj = JsonController().serialize_presence_post(jsondata)
            presence = SendPresenceController(json_obj).getCoTObject()
            return presence

        except Exception as e:
            raise e


class Emergency:

    @staticmethod
    def delete_emergency(json_data: dict) -> object:
        """
        remove an existing emergency

        @rtype: object
        """
        obj = Obj("DELETE")
        jsonobj = serialize_json_to_object(obj, json_data)
        EmergencyObject = SendEmergencyController(jsonobj).getCoTObject()
        return EmergencyObject

    @staticmethod
    def create_emergency(json_data: dict) -> object:
        """

        @rtype: Event
        @param json_data:
        @type json_data: dict
        @return emergency_object:
        """
        json_obj = JsonController().serialize_emergency_post(json_data)
        emergency_object = SendEmergencyController(json_obj).getCoTObject()
        return emergency_object

    @staticmethod
    def get_emergency() -> any:
        """

        @return: a json representation of active emergencies
        """
        output = dbController.query_ActiveEmergency()
        for i in range(0, len(output)):
            original = output[i]
            output[i] = output[i].__dict__
            output[i]["lat"] = original.event.point.lat
            output[i]["lon"] = original.event.point.lon
            output[i]["type"] = original.event.detail.emergency.type
            output[i]["name"] = original.event.detail.contact.callsign
            del (output[i]['_sa_instance_state'])
            del (output[i]['event'])
        return jsonify(json_list=output), 200


class Chat:

    @staticmethod
    def create_chat_to_all(json_data: dict) -> object:
        """ create a chat to all object
        """
        json_obj = JsonController().serialize_chat_post(json_data)
        chat_object = SendChatController(json_obj).getCoTObject()
        return chat_object


@app.route('/Alive')
def sessions():
    return b'API is running', 200


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


@app.route("/ManagePresence")
@auth.login_required()
def ManagePresence():
    pass


@app.route("/ManagePresence/postPresence", methods=[restMethods.POST])
@auth.login_required
def postPresence():
    try:
        global APIPipe
        jsondata = request.get_json(force=True)
        presence = Presence.create_presence(jsondata)
        APIPipe.send(presence)
        return presence.modelObject.getuid(), 200
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
        global APIPipe
        jsondata = request.get_json(force=True)
        simpleCoTObject = GeoObject.create_geoobject(jsondata)
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
        global APIPipe
        jsondata = request.get_json(force=True)
        ChatObject = Chat.create_chat_to_all(jsondata)
        APIPipe.send(ChatObject)
        return 'success', 200
    except Exception as e:
        return str(e), 500


@app.route("/ManageEmergency/getEmergency", methods=[restMethods.GET])
@auth.login_required
def getEmergency():
    try:
        return Emergency.get_emergency()
    except Exception as e:
        return str(e), 200


@app.route("/ManageEmergency/postEmergency", methods=[restMethods.POST])
@auth.login_required
def postEmergency():
    try:
        global APIPipe
        jsondata = request.get_json(force=True)
        EmergencyObject = Emergency.create_emergency(jsondata)
        APIPipe.send(EmergencyObject)
        return EmergencyObject.modelObject.getuid(), 200
    except Exception as e:
        return str(e), 200


@app.route("/ManageEmergency/deleteEmergency", methods=[restMethods.DELETE])
@auth.login_required
def deleteEmergency():
    try:
        global APIPipe
        jsondata = request.get_json(force=True)
        EmergencyObject = Emergency.delete_emergency(jsondata)
        APIPipe.send(EmergencyObject)
        return 'success', 200
    except Exception as e:
        return str(e), 500


@app.route("/ManageEmergency")
@auth.login_required
def listEmergency():
    pass


def serialize_json_to_object(object, json):
    """

    """
    for key in json.keys():
        s = dir(object)
        if key in dir(object):
            setattr(object, str(key), json[key])
        else:
            raise Exception(f'attribute {key} not supported by this endpoint')
    return object


if __name__ == "__main__":
    Emergency().delete_emergency({"uid": "123"})
