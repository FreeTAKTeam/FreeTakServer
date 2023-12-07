from abc import ABC

from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.parsing.load_configuration import LoadConfiguration

class Builder(Controller):
    """manage operations related to mission domain"""
    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.result: any = None
        
    def initialize(self, request, response):
        super().initialize(request, response)
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def build_empty_object(self, config_loader):
        raise NotImplementedError
    
    def add_object_data(self, mapped_object):
        raise NotImplementedError
    
    def get_result(self):
        return self.result
    
    def _create_model_object(self, configuration, extended_domain={}, *args, **kwargs):
        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", extended_domain)

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        model_object = response.get_value("model_object")
        
        return model_object
    