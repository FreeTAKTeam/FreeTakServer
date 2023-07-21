from FreeTAKServer.components.extended.mission.controllers.mission_domain_controller import MissionDomainController
from FreeTAKServer.components.extended.mission.controllers.mission_general_controller import MissionGeneralController
from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import MissionPersistenceController
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

class MissionHierarchyController(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
        ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.persistency_controller = MissionPersistenceController(request, response, sync_action_mapper, configuration)
        self.domain_controller = MissionDomainController(request, response, sync_action_mapper, configuration)
        self.general_controller = MissionGeneralController(request, response, sync_action_mapper, configuration)
        
    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.persistency_controller.initialize(request, response)
        self.domain_controller.initialize(request, response)
        self.general_controller.initialize(request, response)
        
    def add_child_to_parent(self, parent_mission_id: str, child_mission_id: str, *args, **kwargs):
        """add a child mission to a parent"""
        parent_mission = self.persistency_controller.get_mission(parent_mission_id)
        child_mission = self.persistency_controller.get_mission(child_mission_id)
        
        if parent_mission is not None and child_mission is not None:
            self.persistency_controller.add_parent_to_mission(parent_mission=parent_mission, child_mission=child_mission)
            
    def delete_parent(self, child_mission_id: str, *args, **kwargs):
        """delete a parent mission from a child"""
        child_mission = self.persistency_controller.get_mission(child_mission_id)
        if child_mission is not None:
            self.persistency_controller.remove_parent_from_mission(mission_id=child_mission_id, parent_mission=child_mission.parent_missions[0].parent_mission)
        
    def get_children(self, parent_mission_id: str, config_loader, *args, **kwargs):
        """get all the children of a mission"""
        children = self.persistency_controller.get_mission(parent_mission_id).child_missions
        mission_collection = self.domain_controller.create_mission_collection(config_loader)
        for child in children:
            mission_record_domain = self.domain_controller.create_mission_record_object(config_loader)
            self.domain_controller.complete_mission_record_db(mission_record_domain, child.child_mission, config_loader)
            self.domain_controller.add_mission_to_collection(mission_collection, mission_record_domain)
        
        serialized_children = self.general_controller.serialize_to_json(mission_collection)[0]
        self.response.set_value("children", serialized_children)
        return children
        
    def get_parent(self, child_mission_id: str, config_loader, *args, **kwargs):
        """get parent of a mission"""
        mission_collection = self.domain_controller.create_mission_collection(config_loader)
        
        parents = self.persistency_controller.get_mission(child_mission_id).parent_missions
        
        if len(parents)>0:
            parent = parents[0]
            mission_record_domain = self.domain_controller.create_mission_record_object(config_loader)
            
            self.domain_controller.complete_mission_record_db(mission_record_domain, parent.parent_mission, config_loader)
            self.domain_controller.add_mission_to_collection(mission_collection, mission_record_domain)
        else:
            parent = None
            
        serialized_parent = self.general_controller.serialize_to_json(mission_collection)[0]
        self.response.set_value("parent", serialized_parent)
        return parent