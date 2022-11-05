"""this file contains the class with the logic responsible for emergency on events"""

from digitalpy.logic.impl.default_business_rule_controller import (
    DefaultBusinessRuleController,
)

from ..configuration.emergency_constants import (
    CONFIGURATION_PATH_TEMPLATE,
    EMERGENCY_ON_BUSINESS_RULES_PATH,
    EMERGENCY_ALERT,
    BASE_OBJECT_NAME,
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

    def add_call_police_remark(self, **kwargs):
        """this method is to be called by the rule engine to add
        a remark to a given emergency CoT containing the text value
        CALL 911 NOW"""
        self.response.set_values(kwargs)
        self.request.get_value("model_object").detail.remarks.text = "CALL 911 NOW"

    def parse_emergency_on(self, config_loader, **kwargs):
        """this method creates the model object outline and proceeds to pass
        it to the parser to fill the model object with the xml data
        """
        self.request.get_value("logger").debug("parsing emergency off")

        self.response.set_values(kwargs)

        self.request.set_value("object_class_name", BASE_OBJECT_NAME)

        configuration = config_loader.find_configuration(EMERGENCY_ALERT)

        self.request.set_value("configuration", configuration)

        self.request.set_value("source_format", self.request.get_value("source_format"))
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        self.request.set_value("model_object", response.get_value("model_object"))

        # self.request.set_value("message", self.request.get_value("message").xmlString)

        # sub_response = self.execute_sub_action("ParseCoT")
        for key, value in sub_response.get_values().items():
            self.request.set_value(key, value)

        self.request.get_value("logger").debug("emergency on parsed")
