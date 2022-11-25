"""this file contains the class with the logic responsible for emergency on events"""

import pickle
from geopy import distance

from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

from digitalpy.logic.impl.default_business_rule_controller import (
    DefaultBusinessRuleController,
)
from digitalpy.telemetry.tracer import Tracer
from digitalpy.model.load_configuration import Configuration, ConfigurationEntry

from FreeTAKServer.components.core.domain.domain._event import Event
from FreeTAKServer.components.core.domain.domain._dest import dest

from ..configuration.emergency_constants import (
    EMERGENCY_ON_BUSINESS_RULES_PATH,
    EMERGENCY_ALERT,
    BASE_OBJECT_NAME,
)

MAXIMUM_EMERGENCY_DISTANCE = 10
config = MainConfig.instance()


class EmergencyOnController(DefaultBusinessRuleController):
    """this controller is responsible for executing the business logic required
    for proper handling of all Emergency On events"""

    def __init__(
        self,
        request,
        response,
        sync_action_mapper,
        configuration,
        emergency_action_mapper,
    ):

        super().__init__(
            # the path to the business rules used by this controller
            business_rules_path=EMERGENCY_ON_BUSINESS_RULES_PATH,
            # the request object (passed by constructor)
            request=request,
            # the response object (passed by constructor)
            response=response,
            # the configuration object (passed by constructor)
            configuration=configuration,
            # the general action mapper (passed by constructor)
            action_mapper=sync_action_mapper,
            # the component action mapper (passed by constructor).
            # the component or internal action mapper is configured
            # to use the internal action mapping configuration.
            # it is this internal action mapper that is used by
            # the DefaultBusinessRuleController evaluate_request
            internal_action_mapper=emergency_action_mapper,
        )

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def add_call_police_remark(self, tracer: Tracer, **kwargs):
        """this method is to be called by the rule engine to add
        a remark to a given emergency CoT containing the text value
        CALL 911 NOW"""
        with tracer.start_as_current_span("convert_dict_to_node") as span:
            span.add_event("adding remark to emergency on")
            self.request.get_value("model_object").detail.remarks.text = "CALL 911 NOW"

    def retrieve_users(self) -> dict:
        """get the available users"""
        with open(config.UserPersistencePath, "r") as f:
            return pickle.load(f)

    def add_user_to_marti(self, emergency: Event, user: Event):
        """create a new marti dest for the given user to the provided emergency"""
        if not hasattr(emergency.detail, "marti") and not hasattr(
            emergency.detail.marti, "marti"
        ):
            # TODO: this should be done through the domain facade, clarify with @brothercorvo on implementation
            new_dest = dest(Configuration(ConfigurationEntry({})), None)
            new_dest.callsign = user.contact.callsign
            emergency.detail.marti.dest = new_dest

    def filter_by_distance(self, emergency: Event):
        """filter who receives this emergency based on their distance from the emergency"""
        self.users = self.retrieve_users()
        for _, user_obj in self.users.items():
            user_point = user_obj.modelObject.point

            # check that the distance between the user and the emergency is less than 10km
            # TODO: this hardcoded distance should be added to the business rules
            if (
                distance.geodesic(
                    (user_point.lat, user_point.lon),
                    (emergency.point.lat, emergency.point.lon),
                ).km
                < MAXIMUM_EMERGENCY_DISTANCE
            ):
                self.add_user_to_marti(emergency, user_obj.modelObject)

    def parse_emergency_on(self, config_loader, tracer: Tracer, **kwargs):
        """this method creates the model object outline and proceeds to pass
        it to the parser to fill the model object with the xml data
        """
        with tracer.start_as_current_span("convert_dict_to_node") as span:
            span.add_event("parsing emergency on")

            self.request.set_value("object_class_name", BASE_OBJECT_NAME)

            configuration = config_loader.find_configuration(EMERGENCY_ALERT)

            self.request.set_value("configuration", configuration)

            self.request.set_value(
                "source_format", self.request.get_value("source_format")
            )
            self.request.set_value("target_format", "node")

            span.add_event("creating emergency on object")

            response = self.execute_sub_action("CreateNode")

            self.request.set_value("model_object", response.get_value("model_object"))

            for key, value in response.get_values().items():
                self.response.set_value(key, value)
