from digitalpy.logic.impl.default_business_rule_controller import (
    DefaultBusinessRuleController,
)


from ..configuration.drop_point_constants import (
    DROP_POINT_BUSINESS_RULES_PATH,
    BASE_OBJECT_NAME
)


class DropPointController(DefaultBusinessRuleController):

    def __init__(
        self, request, response, action_mapper, configuration, drop_point_action_mapper
    ):

        super().__init__(
            # the path to the business rules used by this controller
            business_rules_path=DROP_POINT_BUSINESS_RULES_PATH,
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
            # the DefaultBusinessRuleController evaluate_request
            internal_action_mapper=drop_point_action_mapper,
        )

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def parse_drop_point(self, **kwargs):
        """Creates the model object outline and 
        """
        self.request.get_value("logger").debug("parsing drop point")

        self.response.set_values(kwargs)

        # TODO
        # self.request.set_value("message_type", EMERGENCY_ALERT)
        self.request.set_value("object_class_name", BASE_OBJECT_NAME)

        self.request.set_context(self.request.get_action())

        response = self.execute_sub_action("CreateNode")

        self.request.set_value("model_object", response.get_value("model_object"))

        self.request.set_value("message", self.request.get_value("message").xmlString)

        sub_response = self.execute_sub_action("ParseCoT")

        for key, value in sub_response.get_values().items():
            self.response.set_value(key, value)