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
        with open(config.UserPersistencePath, "rb") as f:
            return pickle.load(f)

    def add_user_to_marti(self, emergency: Event, user: Event):
        """create a new marti dest for the given user to the provided emergency"""
        self.request.set_value("object_class_name", DEST_CLASS)
        configuration = self.request.get_value("config_loader").find_configuration(DEST_SCHEMA)

        self.request.set_value("configuration", configuration)
        sub_response = self.execute_sub_action("CreateNode")
        new_dest = sub_response.get_value("model_object")
        new_dest.callsign = user.detail.contact.callsign
        emergency.detail.marti.dest = new_dest

    def get_model_object_from_user(self, user) -> Event:
        """user model object can be associated with two variable names
        modelObject or m_presence, this is bandaid for a much bigger issue
        of inconsistent domain usage
        """
        if hasattr(user, "modelObject"):
            return user.modelObject

        elif hasattr(user, "m_presence"):
            return user.m_presence.modelObject

    def filter_by_distance(self, emergency: Event):
        """filter who receives this emergency based on their distance from the emergency"""
        self.users = self.retrieve_users()
        for _, user_obj in self.users.items():
            user_obj = self.get_model_object_from_user(user_obj)
            user_point = user_obj.point

            # check that the distance between the user and the emergency is less than 10km
            # TODO: this hardcoded distance should be added to the business rules
            if (
                distance.geodesic(
                    (user_point.lat, user_point.lon),
                    (emergency.point.lat, emergency.point.lon),
                ).km
                < MAXIMUM_EMERGENCY_DISTANCE
            ):
                self.add_user_to_marti(emergency, user_obj)
