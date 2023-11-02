from abc import ABC
from typing import List, TYPE_CHECKING
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_cot_content_builder import MissionCoTContentBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_standard_external_data_builder import MissionStandardExternalDataBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_list_builder import MissionListBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_list_cot_content_builder import MissionListCoTContentBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_list_record_builder import MissionListRecordBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_standard_content_builder import MissionStandardContentBuilder
from FreeTAKServer.components.extended.mission.persistence.mission import Mission
from FreeTAKServer.core.domain.node import Node

from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.parsing.load_configuration import LoadConfiguration

if TYPE_CHECKING:
    from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject

class MissionDirector(Controller):
    """direct the building of a mission"""
    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        
    def initialize(self, request, response):
        super().initialize(request, response)
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def construct(self, mission: Mission, config_loader, *args, **kwargs) -> Node:
        """construct a node from a mapped object"""
        mission_list_builder = MissionListBuilder(self.request, self.response, self.action_mapper, self.configuration)
        mission_list_builder.initialize(self.request, self.response)
        mission_list_builder.build_empty_object(config_loader, *args, **kwargs)
        mission_list_builder.add_object_data()
        mission_list = mission_list_builder.get_result()

        mission_record_builder = MissionListRecordBuilder(self.request, self.response, self.action_mapper, self.configuration)
        mission_record_builder.initialize(self.request, self.response)
        mission_record_builder.build_empty_object(config_loader, *args, **kwargs)
        mission_record_builder.add_object_data(mission)
        mission_record = mission_record_builder.get_result()
        
        for cot in mission.cots:
            mission_cot_content_builder = MissionCoTContentBuilder(self.request, self.response, self.action_mapper, self.configuration)
            mission_cot_content_builder.initialize(self.request, self.response)
            mission_cot_content_builder.build_empty_object(config_loader, *args, **kwargs)
            mission_cot_content_builder.add_object_data(cot)
            mission_cot_content = mission_cot_content_builder.get_result()
            mission_record.uids = mission_cot_content
        
        for content in mission.contents:

            mission_content_builder = MissionStandardContentBuilder(self.request, self.response, self.action_mapper, self.configuration)
            mission_content_builder.initialize(self.request, self.response)
            mission_content_builder.build_empty_object(config_loader, *args, **kwargs)
            mission_content_builder.add_object_data(content)
            mission_content = mission_content_builder.get_result()
            mission_record.contents = mission_content

        for external_data in mission.externalData:

            mission_external_data_builder = MissionStandardExternalDataBuilder(self.request, self.response, self.action_mapper, self.configuration)
            mission_external_data_builder.initialize(self.request, self.response)
            mission_external_data_builder.build_empty_object(config_loader, *args, **kwargs)
            mission_external_data_builder.add_object_data(external_data)
            mission_external_data = mission_external_data_builder.get_result()
            mission_record.externalData = mission_external_data

        mission_list.data = mission_record
        return mission_list