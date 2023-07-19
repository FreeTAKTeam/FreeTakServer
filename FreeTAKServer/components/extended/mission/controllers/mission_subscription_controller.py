import json
from typing import List, Dict
from FreeTAKServer.components.extended.excheck.domain.mission_info import MissionInfo
from FreeTAKServer.components.extended.mission.controllers.mission_general_controller import MissionGeneralController
from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import MissionPersistenceController
from FreeTAKServer.components.extended.mission.controllers.mission_domain_controller import MissionDomainController
from FreeTAKServer.components.extended.mission.controllers.mission_token_controller import MissionTokenController
from FreeTAKServer.components.extended.mission.domain.external_data import ExternalData
from FreeTAKServer.components.extended.mission.domain.mission_role import MissionRole
from FreeTAKServer.components.extended.mission.domain.mission_subscription import MissionSubscription
from FreeTAKServer.components.extended.mission.persistence.permission import Permission
from FreeTAKServer.components.extended.mission.persistence.role_permission import RolePermission
from FreeTAKServer.components.extended.mission.persistence.subscription import Subscription
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from FreeTAKServer.core.configuration.MainConfig import MainConfig



from ..configuration.mission_constants import (
    BASE_OBJECT_NAME,
    MISSION_CONTENT,
    MISSION_ITEM,
    MISSION_SUBSCRIPTION,
    MISSION_NOTIFICATION
)

config = MainConfig.instance()

class MissionSubscriptionController(Controller):
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
        
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
        
    def get_mission_subscriptions(self, mission_id, config_loader, *args, **kwargs):
        """this method will retrieve all of the subscriptions associated with a mission
        and return them as a json object
        """
        mission_db_obj = self.persistency_controller.get_mission(mission_id)
        subscriptions: List[Subscription] = mission_db_obj.mission_subscriptions
        mission_subscriptions_domain = self.domain_controller.create_mission_subscriptions_list(config_loader)
        completed_subscription_domain = self.complete_mission_subscription_object(mission_subscriptions_domain, subscriptions, config_loader)
        serialized_object = self.general_controller.serialize_to_json(completed_subscription_domain)[0]
        
        self.response.set_value("mission_subscriptions", serialized_object)
        
        return serialized_object
        
    def complete_mission_subscription_object(self, subscriptions_domain_obj: MissionInfo, subscriptions_db_obj: List[Subscription], config_loader, *args, **kwargs) -> MissionInfo:
        """_summary_
        """
        subscriptions_domain_obj.version = "3"
        subscriptions_domain_obj.type = "MissionSubscription"
        subscriptions_domain_obj.nodeId = config.nodeID
        for subscription in subscriptions_db_obj:
            subscription_obj = self.domain_controller.creation_mission_subscription(config_loader)
            subscription_obj.createTime = subscription.createTime
            subscription_obj.clientUid = subscription.clientUid
            subscription_obj.username = subscription.username
            role: MissionRole = subscription_obj.role # type: ignore
            role.permissions = self.get_permissions_as_list(subscription.role.permissions)
            subscriptions_domain_obj.data = subscription_obj
        
        return subscriptions_domain_obj
    
    def get_permissions_as_list(self, role_permissions: List[RolePermission], *args, **kwargs) -> List[str]:
        """get the permissions as a list of strings
        """
        string_permissions: List[str] = []
        
        for role_permission in role_permissions:
            string_permissions.append(role_permission.permission.permission_type)
            
        return string_permissions