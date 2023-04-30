from typing import Dict
from flask import request
from flask_httpauth import HTTPTokenAuth
from digitalpy.core.main.object_factory import ObjectFactory

from FreeTAKServer.services.rest_api_service.views.base_view import BaseView
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.parsers.JsonController import JsonController
from FreeTAKServer.core.persistence.DatabaseController import DatabaseController

from FreeTAKServer.core.RestMessageControllers.SendEmergencyController import SendEmergencyController
from .emergency_persistence import EmergencyPersistence

loggingConstants = LoggingConstants(log_name="FTS-ManageEmergencyView")
logger = CreateLoggerController("FTS-ManageEmergencyView", logging_constants=loggingConstants).getLogger()

class ManageEmergency(BaseView):
    
    def __init__(self, request, response, action_mapper, configuration) -> None:
        endpoints = {
            "getEmergency": self.get_emergency,
            "postEmergency": self.post_emergency,
            "deleteEmergency": self.delete_emergency,
        }
        self.emergency_persistence = EmergencyPersistence(request, response, action_mapper, configuration)
        self.emergency_persistence.initialize(request,response)
        super().__init__(request, response, action_mapper, configuration)
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def get_emergency(self,**kwargs):
        """method to retrieve all emergency's
        Returns:
            str: returns a json string containing dictionary of emergency's

        """
        self.emergency_persistence.get_all_emergencies()
        emergencies = self.response.get_value("emergencies")
        output = {"json_list": []}
        for emergency in emergencies:
            try:
                serialized_emergency = {
                    "lat": emergency.point.lat,
                    "lon": emergency.point.lon,
                    "type": emergency.detail.emergency.type,
                    "name": emergency.detail.contact.callsign,
                    "uid": emergency.uid
                }
                output["json_list"].append(serialized_emergency)
            except AttributeError as ex:
                logger.error("emergency model object missing attribute %s", ex)
        self.response.set_values(output)

    def post_emergency(self):
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_emergency_post(jsondata)
        self.make_request("EmergencyAlert", {"dictionary": jsonobj}, False, "tcp_cot_service") # send the request output to the tcp cot service
        self.make_request("EmergencyAlert", {"dictionary": jsonobj}, False, "ssl_cot_service") # send the request output to the ssl cot service
        return jsonobj.get("@uid"), 200

    def delete_emergency(self) -> str:
        """delete an emergency from the emergency persistence
        """
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_emergency_delete(jsondata)
        self.make_request("EmergencyCancelled", {"dictionary": jsonobj}, False, "tcp_cot_service") # send the request output to the tcp cot service
        self.make_request("EmergencyCancelled", {"dictionary": jsonobj}, False, "ssl_cot_service") # send the request output to the ssl cot service
        return jsonobj.get("@uid"), 200
