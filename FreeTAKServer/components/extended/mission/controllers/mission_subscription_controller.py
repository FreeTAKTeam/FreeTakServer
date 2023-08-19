import json
from typing import List, Dict
from FreeTAKServer.components.extended.excheck.domain.mission_info import MissionInfo
from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import MissionPersistenceController
from FreeTAKServer.components.extended.mission.controllers.mission_domain_controller import MissionDomainController
from FreeTAKServer.components.extended.mission.controllers.mission_token_controller import MissionTokenController
from FreeTAKServer.components.core.domain.domain import MissionInfoSingle
from FreeTAKServer.components.core.domain.domain import MissionRole
from FreeTAKServer.components.extended.mission.persistence.permission import Permission
from FreeTAKServer.components.extended.mission.persistence.role_permission import RolePermission
from FreeTAKServer.components.extended.mission.persistence.subscription import Subscription
from FreeTAKServer.core.util.serialization_utils import serialize_to_json
from FreeTAKServer.core.util.time_utils import get_dtg
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
    MISSION_SUBSCRIPTION_DATA,
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
        self.token_controller = MissionTokenController(request, response, sync_action_mapper, configuration)
        
    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.persistency_controller.initialize(request, response)
        self.domain_controller.initialize(request, response)
        self.token_controller.initialize(request, response)
        
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
        
    def get_all_subscriptions(self, config_loader, *args, **kwargs):
        subscriptions = self.persistency_controller.get_all_subscriptions()
        mission_subscriptions_domain = self.domain_controller.create_mission_subscriptions_list(config_loader)
        completed_subscription_domain = self.complete_mission_subscription_list_object(mission_subscriptions_domain, subscriptions, config_loader)
        serialized_object = serialize_to_json(completed_subscription_domain, self.request, self.execute_sub_action)
        
        self.response.set_value("mission_subscriptions", serialized_object)
        
        return serialized_object
        
    def get_mission_subscriptions(self, mission_id, config_loader, *args, **kwargs):
        """this method will retrieve all of the subscriptions associated with a mission
        and return them as a json object
        """
        mission_db_obj = self.persistency_controller.get_mission(mission_id)
        subscriptions: List[Subscription] = mission_db_obj.mission_subscriptions
        mission_subscriptions_domain = self.domain_controller.create_mission_subscription_simple_list(config_loader)
        completed_subscription_domain = self.complete_mission_subscription_simple_list_object(mission_subscriptions_domain, subscriptions, config_loader)
        serialized_object = serialize_to_json(completed_subscription_domain, self.request, self.execute_sub_action)
        
        self.response.set_value("mission_subscriptions", serialized_object)
        
        return serialized_object
        
    def add_mission_subscription(self, mission_id: str, client: str, topic: str, password: str, secago: str, start: str, end: str, config_loader, *args, **kwargs):
        """add a subscription to a mission

        Args:
            mission_id (str): the id of the mission to add the subscription to
            client (str): the uid of the client who owns the subscription
            topic (str): _description_
            password (str): _description_
            secago (str): _description_
            start (str): _description_
            end (str): _description_
            config_loader (_type_): _description_
        """
        mission_db_obj = self.persistency_controller.get_mission(mission_id)
        
        if mission_db_obj is not None:
            token = self.token_controller.get_token(mission_db_obj)
            
            subscription_db_obj = self.persistency_controller.create_subscription(None, str(mission_id), token, client, mission_db_obj.defaultRole)
            
            domain_subscription = self.domain_controller.create_mission_subscription(config_loader)
            
            completed_subscription = self.complete_mission_subscription(domain_subscription, subscription_db_obj, config_loader)
                
            serialized_object = serialize_to_json(completed_subscription, self.request, self.execute_sub_action)
            
            self.response.set_value("mission_subscription", serialized_object)
        else:
            self.response.set_value("mission_subscription", None)
            
        return serialized_object
            
    def delete_mission_subscription(self, mission_id: str, client: str, topic:str, disconnect_only:str, config_loader, *args, **kwargs):
        mission_db_obj = self.persistency_controller.get_mission(mission_id)
        self.persistency_controller.delete_subscription(mission_db_obj, client)
        self.response.set_value("complete", "true")
    
    def get_mission_subscription(self, mission_id: str, client: str, config_loader, *args, **kwargs):
        
        mission_db_obj = self.persistency_controller.get_mission(mission_id)
        subscription_db_obj = self.persistency_controller.get_subscription(mission_db_obj, client)
        
        domain_subscription = self.domain_controller.create_mission_subscription(config_loader)
        completed_subscription = self.complete_mission_subscription(domain_subscription, subscription_db_obj, config_loader)
        serialized_object = serialize_to_json(completed_subscription, self.request, self.execute_sub_action)
        
        self.response.set_value("mission_subscription", serialized_object)
        return serialized_object
        
    def complete_mission_subscription(self, subscription_domain_obj: MissionInfoSingle, subscription_db_obj: Subscription, config_loader, *args, **kwargs) -> MissionInfoSingle:
        """_summary_
        """
        subscription_domain_obj.version = "3"
        subscription_domain_obj.type = "com.bbn.marti.sync.model.MissionSubscription"
        subscription_domain_obj.nodeId = config.nodeID
        if subscription_domain_obj.data is not None:
            subscription_domain_obj.data.token = subscription_db_obj.token
            subscription_domain_obj.data.clientUid = subscription_db_obj.clientUid
            subscription_domain_obj.data.username = subscription_db_obj.username
            subscription_domain_obj.data.createTime = get_dtg(subscription_db_obj.createTime)
            subscription_domain_obj.data.role.permissions = self.get_permissions_as_list(subscription_db_obj.role.permissions)
            subscription_domain_obj.data.role.type = subscription_db_obj.role.role_type
        
        return subscription_domain_obj
        
    def complete_mission_subscription_simple_list_object(self, subscriptions_domain_obj: MissionInfo, subscriptions_db_obj: List[Subscription], config_loader, *args, **kwargs) -> MissionInfo:
        """complete the mission subscription simple list object from a list of subscriptions
        """
        subscriptions_domain_obj.version = "3"
        subscriptions_domain_obj.type = "MissionSubscription"
        subscriptions_domain_obj.nodeId = config.nodeID
        for subscription in subscriptions_db_obj:
            subscriptions_domain_obj.data = subscription.clientUid
        
        return subscriptions_domain_obj
        
    def complete_mission_subscription_list_object(self, subscriptions_domain_obj: MissionInfo, subscriptions_db_obj: List[Subscription], config_loader, *args, **kwargs) -> MissionInfo:
        """_summary_
        """
        subscriptions_domain_obj.version = "3"
        subscriptions_domain_obj.type = "MissionSubscription"
        subscriptions_domain_obj.nodeId = config.nodeID
        for subscription in subscriptions_db_obj:
            subscription_obj = self.domain_controller.create_mission_subscription_data(config_loader)
            subscription_obj.createTime = get_dtg(subscription.createTime)
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