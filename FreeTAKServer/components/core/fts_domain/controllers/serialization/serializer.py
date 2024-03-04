from digitalpy.core.logic.impl.default_business_rule_controller import (
    DefaultBusinessRuleController,
)
from ...configuration.domain_constants import (
    SERIALIZATION_BUSINESS_RULES_PATH,
)


class Serializer(DefaultBusinessRuleController):
    """this class is mainly empty as it is the accessor class for all other serializers and the logic is outsourced to the business rules.
    If formats are added serialization support access can and should be added to the business rules. The contents of this class should not
    be modified or expanded."""

    def __init__(
        self, request, response, action_mapper, configuration, domain_action_mapper
    ):

        super().__init__(
            # the path to the business rules used by this controller
            business_rules_path=SERIALIZATION_BUSINESS_RULES_PATH,
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
            internal_action_mapper=domain_action_mapper,
        )

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
