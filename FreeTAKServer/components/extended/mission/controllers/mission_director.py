from abc import ABC
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.core.domain.node import Node

from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.parsing.load_configuration import LoadConfiguration

class Director(Controller):
    """direct all builders"""
    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        
    def initialize(self, request, response):
        super().initialize(request, response)
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def construct(self, builder: Builder, mapped_object: any, config_loader, *args, **kwargs) -> Node:
        """construct a node from a mapped object"""
        builder_instance = builder(self.request, self.response, self.action_mapper, self.configuration)
        builder_instance.initialize(self.request, self.response)
        builder_instance.build_empty_object(config_loader, *args, **kwargs)
        builder_instance.add_object_data(mapped_object)
        return builder_instance.get_result()