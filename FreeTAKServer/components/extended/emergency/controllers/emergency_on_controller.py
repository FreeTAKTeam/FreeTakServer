"""this file contains the class with the logic responsible for emergency on events"""
from ..configuration.emergency_constants import (
    EMERGENCY_ON_BUSINESS_RULES_PATH,
    EMERGENCY_ALERT,
    BASE_OBJECT_NAME,
)

from digitalpy.logic.impl.default_business_rule_controller import (
    DefaultBusinessRuleController,
)


class EmergencyOnController(DefaultBusinessRuleController):
    """this controller is responsible for executing the business logic required
    for proper handling of all Emergency On events"""

    def __init__(
        self, request, response, action_mapper, configuration, emergency_action_mapper
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
            action_mapper=action_mapper,
            # the component action mapper (passed by constructor).
            # the component or internal action mapper is configured
            # to use the internal action mapping configuration.
            # it is this internal action mapper that is used by
            # the DefaultBusinessRuleController evaluate_requ
            internal_action_mapper=emergency_action_mapper,
        )

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def parse_emergency_on(self, **kwargs):
        """this method creates the model object outline and proceeds to pass
        it to the parser to fill the model object with the xml data
        """
        self.request.get_value("logger").debug("parsing emergency off")

        self.response.set_values(kwargs)

        self.request.set_value("message_type", EMERGENCY_ALERT)
        self.request.set_value("object_class_name", BASE_OBJECT_NAME)

        # here we are setting the context to be the action, this allows us to create action keys
        # which are not subject to the calling controller. This is particularly important in the
        # context of the CreateNode action because what happens is that when the EmergencyDomain controller
        # is initialized the response sender becomes EmergencyDomain. In the case of the CreateNode action
        # this means that the next action key found is ??CreateNode instead of EmergencyOnController??CreateNode
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
