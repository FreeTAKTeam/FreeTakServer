"""this file contains the class with the logic responsible for emergency on events"""

import pickle
from geopy import distance

from FreeTAKServer.core.configuration.MainConfig import MainConfig

from digitalpy.core.logic.impl.default_business_rule_controller import (
    DefaultBusinessRuleController,
)
from digitalpy.core.telemetry.tracer import Tracer
from digitalpy.core.parsing.load_configuration import Configuration, ConfigurationEntry

from FreeTAKServer.components.core.domain.domain._event import Event
from ..domain import emergency

from ..configuration.emergency_constants import (
    EMERGENCY_ON_BUSINESS_RULES_PATH,
    EMERGENCY_ALERT,
    BASE_OBJECT_NAME,
)

from .emergency_general_controller import EmergencyGeneralController

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
        self.emergency_general_controller = EmergencyGeneralController(request, response, sync_action_mapper, configuration)
        self.emergency_general_controller.initialize(request, response)

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

    def parse_emergency_on(self, config_loader, tracer: Tracer, **kwargs):
        """this method creates the model object outline and proceeds to pass
        it to the parser to fill the model object with the xml data
        """
        with tracer.start_as_current_span("convert_dict_to_node") as span:
            span.add_event("parsing emergency on")

            self.request.set_value("object_class_name", BASE_OBJECT_NAME)

            configuration = config_loader.find_configuration(EMERGENCY_ALERT)

            self.request.set_value("configuration", configuration)

            self.request.set_value("extended_domain", {"emergency": emergency})

            self.request.set_value(
                "source_format", self.request.get_value("source_format")
            )
            self.request.set_value("target_format", "node")

            span.add_event("creating emergency on object")

            response = self.execute_sub_action("CreateNode")

            self.request.set_value("model_object", response.get_value("model_object"))

            response = self.execute_sub_action("DictToNode")

            for key, value in response.get_values().items():
                self.response.set_value(key, value)

            self.request.set_value('message', response.get_value("model_object"))
            # Serializer called by service manager requires the message value
            self.response.set_value('message', response.get_value("model_object"))
            self.request.set_value('recipients', [])

            self.emergency_general_controller.initialize(self.request, self.response)
            self.emergency_general_controller.filter_by_distance(response.get_value("model_object"))
            self.emergency_general_controller.convert_type(self.response.get_value('message'))

            # validate the users in the recipients list
            response = self.execute_sub_action("ValidateUsers")

            for key, value in response.get_values().items():
                self.response.set_value(key, value)
            
            self.response.set_action("publish")
