from FreeTAKServer.components.core.abstract_component.facade import Facade
from FreeTAKServer.components.core.xml_serializer.configuration.xml_serializer_constants import (
    ACTION_MAPPING_PATH,
    TYPE_MAPPINGS,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
)
from . import base


class XmlSerializer(Facade):
    """Facade class for the Component component. Responsible for handling all public routing.
    Forwards all requests to the internal router.
    """

    def __init__(
        self,
        xml_serializer_action_mapper,
        request,
        response,
        configuration,
    ):
        super().__init__(
            # the path to the external action mapping
            action_mapping_path=ACTION_MAPPING_PATH,
            # the path to the internal action mapping
            internal_action_mapping_path=INTERNAL_ACTION_MAPPING_PATH,
            # the type mapping in dictionary form
            type_mapping=TYPE_MAPPINGS,
            # the path to the logger configuration
            logger_configuration=LOGGING_CONFIGURATION_PATH,
            # the package containing the base classes
            base=base,
            # the component specific action mapper (passed by constructor)
            action_mapper=xml_serializer_action_mapper,
            # the request object (passed by constructor)
            request=request,
            # the response object (passed by constructor)
            response=response,
            # the configuration object (passed by constructor)
            configuration=configuration,
        )
