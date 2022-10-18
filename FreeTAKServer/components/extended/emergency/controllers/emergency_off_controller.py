"""this file contains the class with the logic responsible for emergency off events"""
from digitalpy.logic.impl.default_business_rule_controller import (
    DefaultBusinessRuleController,
)

from ..configuration.emergency_constants import (
    EMERGENCY_OFF_BUSINESS_RULES_PATH,
    EMERGENCY_OFF,
    BASE_OBJECT_NAME,
)


class EmergencyOffController(DefaultBusinessRuleController):
    """this controller is responsible for executing the business logic required
    for proper handling of all Emergency Off events"""

    def __init__(
        self,
        request,
        response,
        sync_action_mapper,
        configuration,
        emergency_action_mapper,
    ):

        super().__init__(
            business_rules_path=EMERGENCY_OFF_BUSINESS_RULES_PATH,
            request=request,
            response=response,
            configuration=configuration,
            action_mapper=sync_action_mapper,
            internal_action_mapper=emergency_action_mapper,
        )

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def parse_emergency_off(self, **kwargs):
        """this method creates the model object outline and proceeds to pass
        it to the parser to fill the model object with the xml data"""
        self.request.get_value("logger").debug("parsing emergency off")

        self.response.set_values(kwargs)

        self.request.set_value("message_type", EMERGENCY_OFF)
        self.request.set_value("object_class_name", BASE_OBJECT_NAME)

        # here we are setting the context to be the action, this allows us to create action keys
        # which are not subject to the calling controller. This is particularly important in the
        # context of the CreateNode action because what happens is that when the EmergencyDomain controller
        # is initialized the response sender becomes EmergencyDomain. In the case of the CreateNode action
        # this means that the next action key found is ??CreateNode instead of EmergencyOffController??CreateNode
        # resulting in a failing call to ??CreateNode. By setting the context to be the action,
        # we can now set the routing key to be ?[previous action]?CreateNode which is not impacted by the sender
        # and therefore ends after being called without any subsequent actions.
        self.request.set_context(self.request.get_action())
        response = self.execute_sub_action("CreateNode")

        self.request.set_value("model_object", response.get_value("model_object"))

        self.request.set_value("message", self.request.get_value("message").xmlString)

        sub_response = self.execute_sub_action("ParseCoT")

        for key, value in sub_response.get_values().items():
            self.response.set_value(key, value)

        self.request.get_value("logger").debug("emergency off parsed")
