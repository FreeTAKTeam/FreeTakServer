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

    def parse_emergency_off(self, config_loader, **kwargs):
        """this method creates the model object outline and proceeds to pass
        it to the parser to fill the model object with the xml data"""
        self.request.get_value("logger").debug("parsing emergency off")

        self.response.set_values(kwargs)

        self.request.set_value("object_class_name", BASE_OBJECT_NAME)

        configuration = config_loader.find_configuration(EMERGENCY_OFF)

        self.request.set_value("configuration", configuration)

        self.request.set_value("source_format", self.request.get_value("source_format"))
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        self.request.set_value("model_object", response.get_value("model_object"))

        for key, value in response.get_values().items():
            self.response.set_value(key, value)

        self.request.get_value("logger").debug("emergency off parsed")
