from abc import ABC
from typing import List, TYPE_CHECKING
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_cot_content_builder import MissionCoTContentBuilder
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

class MissionListDirector(Controller):
    """direct the building of mission lists"""
    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        
    def initialize(self, request, response):
        super().initialize(request, response)
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def construct(self, missions: List[Mission], config_loader, *args, **kwargs) -> Node:
        """construct a node from a mapped object"""
        mission_list_builder = MissionListBuilder(self.request, self.response, self.action_mapper, self.configuration)
        mission_list_builder.initialize(self.request, self.response)
        mission_list_builder.build_empty_object(config_loader, *args, **kwargs)
        mission_list_builder.add_object_data()
        mission_list = mission_list_builder.get_result()

        for mission in missions:
            mission_list_record_builder = MissionListRecordBuilder(self.request, self.response, self.action_mapper, self.configuration)
            mission_list_record_builder.initialize(self.request, self.response)
            mission_list_record_builder.build_empty_object(config_loader, *args, **kwargs)
            mission_list_record_builder.add_object_data(mission)
            mission_list_record = mission_list_record_builder.get_result()
            
            for cot in mission.cots:
                mission_list_cot_content_builder = MissionListCoTContentBuilder(self.request, self.response, self.action_mapper, self.configuration)
                mission_list_cot_content_builder.initialize(self.request, self.response)
                mission_list_cot_content_builder.build_empty_object(config_loader, *args, **kwargs)
                mission_list_cot_content_builder.add_object_data(cot)
                mission_list_cot_content = mission_list_cot_content_builder.get_result()
                mission_list_record.uids = mission_list_cot_content
            
            for content in mission.contents:

                mission_list_content_builder = MissionStandardContentBuilder(self.request, self.response, self.action_mapper, self.configuration)
                mission_list_content_builder.initialize(self.request, self.response)
                mission_list_content_builder.build_empty_object(config_loader, *args, **kwargs)
                mission_list_content_builder.add_object_data(content)
                mission_list_content = mission_list_content_builder.get_result()
                mission_list_record.contents = mission_list_content

            mission_list.data = mission_list_record
        
        return mission_list