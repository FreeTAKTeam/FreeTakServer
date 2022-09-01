from ..configuration.emergency_constants import (
    EMERGENCY_ON_BUSINESS_RULES_PATH,
    EMERGENCY_ALERT,
    BASE_OBJECT_NAME,
)

from digitalpy.logic.impl.default_business_rule_controller import (
    DefaultBusinessRuleController,
)


class EmergencyOnController(DefaultBusinessRuleController):
    def __init__(
        self, request, response, action_mapper, configuration, emergency_action_mapper
    ):

        super().__init__(
            business_rules_path=EMERGENCY_ON_BUSINESS_RULES_PATH,
            request=request,
            response=response,
            configuration=configuration,
            action_mapper=action_mapper,
            internal_action_mapper=emergency_action_mapper,
        )

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def parse_emergency_on(self, **kwargs):
        self.request.get_value("logger").debug("parsing emergency off")

        self.response.set_values(kwargs)

        self.request.set_value("message_type", EMERGENCY_ALERT)
        self.request.set_value("object_class_name", BASE_OBJECT_NAME)

        response = self.execute_sub_action("CreateNode")

        self.request.set_value("model_object", response.get_value("model_object"))

        self.request.set_value("message", self.request.get_value("message").xmlString)

        sub_response = self.execute_sub_action("ParseCoT")

        for key, value in sub_response.get_values().items():
            self.response.set_value(key, value)
