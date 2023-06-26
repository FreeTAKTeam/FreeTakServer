from FreeTAKServer.services.rest_api_service.views.base_view import BaseView
from typing import Dict
from flask import request

from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.parsers.JsonController import JsonController
from FreeTAKServer.core.RestMessageControllers.SendEmergencyController import SendEmergencyController

loggingConstants = LoggingConstants(log_name="FTS-ManageEmergencyView")
logger = CreateLoggerController("FTS-ManageEmergencyView", logging_constants=loggingConstants).getLogger()

class ManageEmergency(BaseView):
    decorators = []
    
    def __init__(self) -> None:
        endpoints = {
            "getEmergency": self.get_emergency,
            "postEmergency": self.post_emergency,
            "deleteEmergency": self.delete_emergency,
        }
        self.set_endpoints(endpoints=endpoints)
        super().__init__(endpoints)
    
    def get_emergency(self):
        """method to retrieve all emergency's
        Returns:
            str: returns a json string containing dictionary of emergency's

        """
        response = self.make_request("GetAllEmergencies") # retrieve emergencies from the emergency component
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
    
    def post_emergency(self):
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_emergency_post(jsondata)
        self.make_request("EmergencyAlert", {"dictionary": jsonobj}, False, "tcp_cot_service") # send the request output to the tcp cot service
        self.make_request("EmergencyAlert", {"dictionary": jsonobj}, False, "ssl_cot_service") # send the request output to the ssl cot service
        return jsonobj.get("event").get("@uid"), 200 
       
    def delete_emergency(self) -> str:
        """delete an emergency from the emergency persistence

        """
        jsondata = request.get_json(force=True)
        jsonobj = JsonController().serialize_emergency_delete(jsondata)
        self.make_request("EmergencyCancelled", {"dictionary": jsonobj}, False, "tcp_cot_service") # send the request output to the tcp cot service
        self.make_request("EmergencyCancelled", {"dictionary": jsonobj}, False, "ssl_cot_service") # send the request output to the ssl cot service
        return jsonobj.get("@uid"), 200
