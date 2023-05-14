from digitalpy.core.IAM.model.connection import Connection
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.domain.node import Node
from digitalpy.core.parsing.load_configuration import LoadConfiguration

from ..configuration.cot_management_constants import (
    GEO_OBJECT,
    BASE_OBJECT_NAME,
    DELETE_GEO_OBJECT
)

class CotManagementGeoObjectController(Controller):
    """this class is responsible for handling geo objects
    """
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, sync_action_mapper, configuration)

    def initialize(self, request, response):
        self.request = request
        self.response = response
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def delete_geo_object(self, config_loader: LoadConfiguration, **kwargs):
        """create a new delete geo object message

        Args:
            uid (str): the uid of the node to be deleted
            config_loader (LoadConfiguration): a configuration loader instance passed by the facade used
                to load model configurations
        """
        self.response.set_value("object_class_name", BASE_OBJECT_NAME)

        configuration = config_loader.find_configuration(DELETE_GEO_OBJECT)

        self.response.set_value("configuration", configuration)

        self.response.set_action("CreateNode")

        # copy request values to response
        for key, value in self.request.get_values().items():
            self.response.set_value(key, value)

    def create_geo_object(self, config_loader: LoadConfiguration, **kwargs):
        """ create a new geo object

        Args:
            config_loader (LoadConfiguration): a configuration loader instance passed by the facade used
                to load model configurations
        """
        self.response.set_value("object_class_name", BASE_OBJECT_NAME)

        configuration = config_loader.find_configuration(GEO_OBJECT)

        self.response.set_value("configuration", configuration)

        self.response.set_action("CreateNode")

        # copy request values to response
        for key, value in self.request.get_values().items():
            self.response.set_value(key, value)