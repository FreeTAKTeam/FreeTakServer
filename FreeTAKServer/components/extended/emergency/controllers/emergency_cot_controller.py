from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.core.object_factory import ObjectFactory
from digitalpy.logic.impl.default_business_rule_controller import (
    DefaultBusinessRuleController,
)
from ..domain import Event
from ..base.emergency_constants import BASE_OBJECT_NAME, EMERGENCY_OFF, EMERGENCY_ALERT


class EmergencyMain(DefaultBusinessRuleController):
    emergencies = {}

    def __init__(self, request, response, action_mapper, configuration):
        business_rules = {
            "rules": {
                'type != "EmergencyDelete"': {
                    "callbacks": [self._parse_emergency_on],
                    "matchable": "model_object",
                    "rules": {
                        'type == "EmergencyAlert"': {
                            "callbacks": [
                                self._add_emergency_to_emergencies,
                                self.emergency_broadcast,
                            ]
                        },
                        'type == "EmergencyInContact"': {
                            "callbacks": [
                                self._add_emergency_to_emergencies,
                                self.emergency_broadcast,
                            ]
                        },
                        'type == "EmergencyRingTheBell"': {
                            "callbacks": [
                                self._add_emergency_to_emergencies,
                                self.emergency_broadcast,
                            ]
                        },
                        'type == "EmergencyGeoFenceBreached"': {
                            "callbacks": [
                                self._add_emergency_to_emergencies,
                                self.emergency_broadcast,
                            ]
                        },
                        'type == "EmergencyCancelled"': {
                            "callbacks": [
                                self._add_emergency_to_emergencies,
                                self.emergency_broadcast,
                            ]
                        },
                    },
                },
                'type == "EmergencyDelete"': {
                    "callbacks": [self._parse_emergency_on],
                    "matchable": "model_object",
                    "rules": {
                        'type == "EmergencyDelete"': {
                            "callbacks": [
                                self._remove_emergency_from_emergencies,
                                self.emergency_broadcast,
                            ]
                        }
                    },
                },
                'type == "ClientConnected"': {
                    "callbacks": [self.emergency_broadcast_all]
                },
            },
            "matchable": "xml_element",
        }
        super().__init__(
            business_rules=business_rules,
            request=request,
            response=response,
            configuration=configuration,
            action_mapper=action_mapper,
        )

    def accept_visitor(self, visitor):
        pass

    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def _parse_emergency_on(self, **kwargs):
        self.response.set_values(kwargs)

        self.request.set_value("message_type", EMERGENCY_ALERT)
        self.request.set_value("object_class_name", BASE_OBJECT_NAME)

        response = self.execute_sub_action("CreateNode")

        self.request.set_value("model_object", response.get_value("model_object"))

        self.request.set_value("message", self.request.get_value("message").xmlString)

        sub_response = self.execute_sub_action("ParseCoT")

        for key, value in sub_response.get_values().items():
            self.response.set_value(key, value)

    def emergency_broadcast(self, model_object: Event, **kwargs):
        """this method will broadcast a specific emergency

        Args:
            emergency_uid (str): the uid of the emergency to be broadcasted
        """
        try:
            self.request.get_value("logger").debug(
                f"broadcasting emergency {model_object.uid}"
            )

            self.response.set_values(kwargs)
            self.request.set_value("model_objects", [model_object])
            self.execute_sub_action("Broadcast")
        except Exception as error:
            self.request.get_value("logger").error(
                f"error broadcasting emergency {error}"
            )

    def _add_emergency_to_emergencies(self, model_object, **kwargs) -> None:
        """this method adds a new emergency to the list of emergencies

        Args:
            emergency (Event): the new emergency model object
        """
        try:
            emergency_uid = model_object.uid
            self.emergencies[emergency_uid] = model_object
            self.request.get_value("logger").debug(
                f"added emergency: {emergency_uid} to emergencies: {self.emergencies}"
            )
        except Exception as error:
            self.request.get_value("logger").error(
                f"error adding emergency to emergencies {error}"
            )

    def _remove_emergency_from_emergencies(self, emergency) -> None:
        """this method removes the specified emergency from the list of emergencies

        Args:
            emergency (Event): the emergency delete model object
        """
        del self.emergencies[emergency.uid]

    def emergency_received(self, logger, **kwargs):
        """this method is called to handle an emergency received
        Args:
            message (RawCoT): the RawCoT containing the emergency alert message
            logger (logging.Logger): the component logger instance
        """
        try:
            self.response.set_values(kwargs)

            logger.info("emergency alert received")

            facade = ObjectFactory.get_instance(self.request.get_sender())

            empty_model_object = facade.create_node(EMERGENCY_ALERT, BASE_OBJECT_NAME)

            self.request.set_value("model_object", empty_model_object)

            self.request.set_value(
                "message", self.request.get_value("message").xmlString
            )

            emergency_object = self.execute_sub_action("ParseCoT").get_value(
                "model_object"
            )

        except Exception as error:
            logger.error(f"exception in emergency alert: {error}")

    def emergency_broadcast_all(self, **kwargs):
        """this method will broadcast all emergencies
        Args:
        """
        self.response.set_values(kwargs)
        self.response.set_action("Broadcast")
        self.response.set_value("model_objects", list(self.emergencies.values()))

    def emergency_delete(self, message, logger, **kwargs):
        """this method is called to handle an emergency delete message
        Args:
            message (RawCoT): the RawCoT containing the emergency delete message
            logger (logging.Logger): the component logger instance
        """
        try:
            self.response.set_values(kwargs)

            logger.info("emergency delete received")

            facade = ObjectFactory.get_instance(self.request.get_sender())

            empty_model_object = facade.create_node(EMERGENCY_OFF, BASE_OBJECT_NAME)

            self.request.set_value("model_object", empty_model_object)

            self.request.set_value(
                "message", self.request.get_value("message").xmlString
            )

            emergency_object = self.execute_sub_action("ParseCoT").get_value(
                "model_object"
            )

        except Exception as error:
            logger.error(f"exception in emergency delete: {error}")
