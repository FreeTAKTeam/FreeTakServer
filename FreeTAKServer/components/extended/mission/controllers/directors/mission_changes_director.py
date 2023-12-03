from abc import ABC
from typing import List, TYPE_CHECKING
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_content_change_builder import MissionContentChangeBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_change_list_builder import MissionChangeListBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_external_data_change_builder import MissionExternalDataChangeBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_simple_change_builder import MissionSimpleChangeBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_simple_cot_change_builder import MissionSimpleCoTChangeBuilder
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

class MissionChangesDirector(Controller):
    """direct the building of mission changes"""
    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        
    def initialize(self, request, response):
        super().initialize(request, response)
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def construct(self, mission: Mission, config_loader, *args, **kwargs) -> Node:
        """construct a node from a mapped object"""
        mission_change_list_builder = MissionChangeListBuilder(self.request, self.response, self.action_mapper, self.configuration)
        mission_change_list_builder.initialize(self.request, self.response)
        mission_change_list_builder.build_empty_object(config_loader, *args, **kwargs)
        mission_change_list_builder.add_object_data()
        mission_change_list = mission_change_list_builder.get_result()

        for change in mission.changes:
            if change.content_resource_uid != None:
                mission_change_record = MissionContentChangeBuilder(self.request, self.response, self.action_mapper, self.configuration)
                mission_change_record.initialize(self.request, self.response)
                mission_change_record.build_empty_object(config_loader, *args, **kwargs)
                mission_change_record.add_object_data(change)
                mission_change = mission_change_record.get_result()
                mission_change_list.data = mission_change
                
            elif change.cot_detail_uid != None:
                mission_change_record = MissionSimpleCoTChangeBuilder(self.request, self.response, self.action_mapper, self.configuration)
                mission_change_record.initialize(self.request, self.response)
                mission_change_record.build_empty_object(config_loader, *args, **kwargs)
                mission_change_record.add_object_data(change)
                mission_change = mission_change_record.get_result()
                mission_change_list.data = mission_change

            elif change.external_data_uid != None:
                mission_change_record = MissionExternalDataChangeBuilder(self.request, self.response, self.action_mapper, self.configuration)
                mission_change_record.initialize(self.request, self.response)
                mission_change_record.build_empty_object(config_loader, *args, **kwargs)
                mission_change_record.add_object_data(change)
                mission_change = mission_change_record.get_result()
                mission_change_list.data = mission_change

            else:
                mission_change_record = MissionSimpleChangeBuilder(self.request, self.response, self.action_mapper, self.configuration)
                mission_change_record.initialize(self.request, self.response)
                mission_change_record.build_empty_object(config_loader, *args, **kwargs)
                mission_change_record.add_object_data(change)
                mission_change = mission_change_record.get_result()
                mission_change_list.data = mission_change

        return mission_change_list