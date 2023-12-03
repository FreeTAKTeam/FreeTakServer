import json
from typing import List
import uuid
from flask import Blueprint, request, make_response

from FreeTAKServer.core.RestMessageControllers.RestEnumerations import RestEnumerations
from ..controllers.authentication import auth
from geopy import Point, distance, Nominatim
import datetime as dt

from FreeTAKServer.core.util.time_utils import get_current_dtg
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.parsers.JsonController import JsonController
from FreeTAKServer.core.RestMessageControllers.SendSimpleCoTController import SendSimpleCoTController
from FreeTAKServer.services.rest_api_service.controllers.rest_api_communication_controller import RestAPICommunicationController
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController

config = MainConfig.instance()
page = Blueprint('emergency', __name__)

loggingConstants = LoggingConstants(log_name="FTS-RestAPI_Service")
logger = CreateLoggerController("FTS-RestAPI_Service", logging_constants=loggingConstants).getLogger()

@page.route('/ManageEmergency/getEmergency', methods=['GET'])
@auth.login_required
def get_emergencys():
    """method to retrieve all emergency's
    Returns:
        str: returns a json string containing dictionary of emergency's

    """
    response = RestAPICommunicationController().make_request("GetAllEmergencies", "emergency", {}, None, True) # retrieve emergencies from the emergency component
    emergencies = response.get_value("emergencies")
    output = {"json_list": []}
    for emergency in emergencies:
        try:
            name = emergency.detail.contact.callsign
            if emergency.detail.contact.callsign is None:
                name = emergency.detail.emergency.text
            serialized_emergency = {
                "lat": emergency.point.lat,
                "lon": emergency.point.lon,
                "type": emergency.detail.emergency.type,
                "name": name,
                "uid": emergency.uid
            }
            output["json_list"].append(serialized_emergency)
        except AttributeError as ex:
            logger.error("emergency model object missing attribute %s", ex)
    return output
    
@page.route('/ManageEmergency/postEmergency', methods=['POST'])
@auth.login_required
def post_emergency():
    jsondata = request.get_json(force=True)
    jsonobj = JsonController().serialize_emergency_post(jsondata)
    RestAPICommunicationController().make_request("EmergencyAlert", "emergency", {"dictionary": jsonobj}, "tcp_cot_service", synchronous = False) # send the request output to the tcp cot service
    RestAPICommunicationController().make_request("EmergencyAlert", "emergency", {"dictionary": jsonobj}, "ssl_cot_service", synchronous = False) # send the request output to the ssl cot service
    return {"message":jsonobj.get("event").get("@uid")}, 200

@page.route('/ManageEmergency/deleteEmergency', methods=['DELETE'])
@auth.login_required
def delete_emergency():
    """delete an emergency from the emergency persistence
    """
    jsondata = request.get_json(force=True)
    jsonobj = JsonController().serialize_emergency_delete(jsondata)
    RestAPICommunicationController().make_request("EmergencyCancelled", "emergency", {"dictionary": jsonobj}, False, "tcp_cot_service") # send the request output to the tcp cot service
    RestAPICommunicationController().make_request("EmergencyCancelled", "emergency", {"dictionary": jsonobj}, False, "ssl_cot_service") # send the request output to the ssl cot service
    return {"message":jsonobj.get("@uid")}, 200
