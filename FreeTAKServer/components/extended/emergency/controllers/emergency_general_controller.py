from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from ..configuration.emergency_constants import (
    DEST_SCHEMA,
    DEST_CLASS,
    MAXIMUM_EMERGENCY_DISTANCE
)

from FreeTAKServer.components.core.domain.domain._event import Event
from FreeTAKServer.core.configuration.MainConfig import MainConfig
import pickle
from geopy import distance

config = MainConfig.instance()

class EmergencyGeneralController(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ):
        super().__init__(request, response, sync_action_mapper, configuration)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def serialize_emergency(self, **kwargs):
        """this is the general method used to serialize the emergency to a given format"""
        # serialize the emergency model object in a sub-action
        response = self.execute_sub_action(
            self.request.get_value("model_object_parser")
        )
        # add the serialized model object to the controller response as a value
        self.response.set_value(
            "serialized_message", response.get_value("serialized_message")
        )
        self.request.get_value("logger").debug(
            "serialized emergency message to format "
            + self.request.get_value("model_object_parser")
        )
        
    def retrieve_users(self) -> dict:
        """get the available users"""
        sub_response = self.execute_sub_action("GetAllConnections")
        return sub_response.get_value("connections")

    def convert_type(self, model_object, **kwargs)->None:
        """convert the model_object type from machine readable to human readable"""
        self.request.set_value("human_readable_type", model_object.type)
        response = self.execute_sub_action("ConvertHumanReadableToMachineReadable")
        model_object.type = response.get_value("machine_readable_type")

    def filter_by_distance(self, emergency: Event):
        """filter who receives this emergency based on their distance from the emergency"""
        self.connections = self.retrieve_users()
        for _, connection_obj in self.connections.items():
            connection_model_object = connection_obj.model_object
            connection_location = connection_model_object.point

            # check that the distance between the user and the emergency is less than 10km
            # TODO: this hardcoded distance should be added to the business rules
            if (
                MAXIMUM_EMERGENCY_DISTANCE==0 or
                distance.geodesic(
                    (connection_location.lat, connection_location.lon),
                    (emergency.point.lat, emergency.point.lon),
                ).km
                < MAXIMUM_EMERGENCY_DISTANCE
            ):
                self.request.get_value('recipients').append(str(connection_obj.get_oid()))
