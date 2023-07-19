from typing import TYPE_CHECKING

from FreeTAKServer.components.extended.mission.domain.mission_log import MissionLog

if TYPE_CHECKING:
    from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject

from FreeTAKServer.components.core.domain.domain import Event
from FreeTAKServer.components.extended.mission.domain.mission_subscription import MissionSubscription
from FreeTAKServer.core.configuration.MainConfig import MainConfig

from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.parsing.load_configuration import LoadConfiguration

from ..domain.mission_info import MissionInfo
from ..domain.mission_data import MissionData
from ..domain.external_data import ExternalData
from ..domain.mission_role import MissionRole
from ..domain.mission_content_data import MissionContentData 
from ..domain.mission_content import MissionContent
from ..domain.mission import mission as DomainMissionCot

from ..persistence.mission import Mission as DBMission
from ..persistence.mission_content import MissionContent as DBMissionContent
from ..persistence.subscription import Subscription as DBSubscription

from ..configuration.mission_constants import (
    BASE_OBJECT_NAME,
    MISSION_CONTENT,
    MISSION_ITEM,
    MISSION_LOG,
    MISSION_LOG_COLLECTION,
    MISSION_RECORD,
    MISSION_SUBSCRIPTION,
    MISSION_NOTIFICATION,
    MISSION_COLLECTION,
    MISSION_SUBSCRIPTION_LIST
)

config = MainConfig.instance()

class MissionDomainController(Controller):
    """manage operations related to mission domain"""
    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        
    def initialize(self, request, response):
        super().initialize(request, response)
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def create_mission_collection(self, config_loader, *args, **kwargs) -> MissionInfo:
        """create a new empty mission collection"""
        self.request.set_value("object_class_name", "MissionInfo")
        
        configuration = config_loader.find_configuration(MISSION_COLLECTION)
        
        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"MissionInfo": MissionInfo})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        mission_collection: MissionInfo = response.get_value("model_object")
        
        mission_collection.version = "3"
        mission_collection.type = "Mission"
        mission_collection.nodeId = config.nodeID
        
        return response.get_value("model_object")
    
    def add_mission_to_collection(self, mission_collection:MissionInfo, mission_record:MissionData, *args, **kwargs) -> MissionData:
        """add a mission record to a mission collection"""
        mission_collection.data = mission_record
        return mission_collection
        
    def create_mission_record_object(self, config_loader: LoadConfiguration, **kwargs):
        """create a new mission subscription object"""
        self.request.set_value("object_class_name", "MissionData")

        configuration = config_loader.find_configuration(MISSION_RECORD)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"MissionData": MissionData, "MissionContent": MissionContent, "MissionContentData": MissionContentData, "ExternalData": ExternalData, "MissionRole": MissionRole})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")
    
    def complete_mission_record_db(self, mission_domain_object: MissionData, mission_db_object: DBMission, config_loader, subscription: DBSubscription = None, **kwargs) -> MissionData: # type: ignore
        """complete the mission record from a db object"""
        # complete the mission record db object
        mission_domain_object.name = mission_db_object.PrimaryKey
        mission_domain_object.description = mission_db_object.description
        mission_domain_object.chatRoom = mission_db_object.chatRoom
        mission_domain_object.baseLayer = mission_db_object.baseLayer
        mission_domain_object.bbox = mission_db_object.bbox
        mission_domain_object.path = mission_db_object.path
        mission_domain_object.classification = mission_db_object.classification
        mission_domain_object.tool = "public"
        # mission_domain_object.keywords = mission_db_object.keywords
        mission_domain_object.keywords = []
        mission_domain_object.creatorUid = mission_db_object.creatorUid
        # TODO: get time dynamically
        mission_domain_object.createTime = "2023-02-22T16:06:26.979Z"
        # mission_domain_object.groups = mission_db_object.groups
        mission_domain_object.groups = []
        # mission_domain_object.externalData = mission_db_object.externalData
        mission_domain_object.externalData = []
        # mission_domain_object.feeds = mission_db_object.feeds
        mission_domain_object.feeds = []
        # mission_domain_object.mapLayers = mission_db_object.mapLayers
        mission_domain_object.mapLayers = []
        mission_domain_object.inviteOnly = mission_db_object.inviteOnly
        mission_domain_object.expiration = mission_db_object.expiration
        # mission_domain_object.uids = mission_db_object.uids
        mission_domain_object.uids = []
        mission_domain_object.passwordProtected = mission_db_object.passwordProtected
        
        for db_content in mission_db_object.contents:
            domain_content = self.create_mission_content(config_loader)
            mission_domain_object.contents = self.complete_mission_content_db(domain_content, db_content)
        
        if subscription is not None:
            mission_domain_object.token = subscription.token
        
        return mission_domain_object
    
    def create_mission_creation_notification(self, config_loader,*args, **kwargs):
        """create a new mission notification object"""
        self.request.set_value("object_class_name", "Event")

        configuration = config_loader.find_configuration(MISSION_NOTIFICATION)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"mission": DomainMissionCot})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        model_object = response.get_value("model_object")

        return model_object
    
    def complete_mission_content_db(self, mission_content_domain: MissionContent, mission_content_db: DBMissionContent, *args, **kwargs) -> MissionContent:
        self.request.set_value("objectuid", mission_content_db.PrimaryKey)
        self.request.set_value("objecthash", mission_content_db.PrimaryKey)
        
        enterprise_sync_db: 'EnterpriseSyncDataObject' = self.execute_sub_action("GetEnterpriseSyncMetaData").get_value("objectmetadata")
        
        mission_content_domain.timestamp = enterprise_sync_db.start_time
        mission_content_domain.creatorUid = enterprise_sync_db.creator_uid
        
        mission_content_domain.data.uid = enterprise_sync_db.PrimaryKey
        mission_content_domain.data.hash = enterprise_sync_db.hash
        mission_content_domain.data.name = enterprise_sync_db.file_name
        mission_content_domain.data.mimeType = enterprise_sync_db.mime_type
        mission_content_domain.data.size = enterprise_sync_db.length
        mission_content_domain.data.tool = enterprise_sync_db.tool
        mission_content_domain.data.submitter = enterprise_sync_db.submitter
        
        keywords = []
        for keyword in enterprise_sync_db.keywords:
            keywords.append(keyword.keyword)
            
        mission_content_domain.data.keywords = keywords
        mission_content_domain.data.expiration = enterprise_sync_db.expiration
        
        return mission_content_domain
    
    def complete_mission_creation_notification(self, mission_notification: Event, mission: MissionData, *args, **kwargs) -> Event:
        """complete a mission creation notification object based on a mission domain object

        Args:
            mission_notification (Event): the mission notification object to complete
            mission (MissionData): the mission domain object to use for completion
        """
        mission_notification.type = "t-x-m-n" # type: ignore
        mission_notification.how = "h-g-i-g-o" # type: ignore
        mission_notification.detail.mission.type = "CREATE" # type: ignore
        mission_notification.detail.mission.tool = "public" # type: ignore
        mission_notification.detail.mission.name = mission.name # type: ignore
        mission_notification.detail.mission.authorUid = mission.creatorUid # type: ignore
        
        return mission_notification
    
    def create_mission_subscriptions_list(self, config_loader, *args, **kwargs) -> MissionInfo:
        """return the domain object used to show all the subscriptions in a mission"""
        self.request.set_value("object_class_name", "MissionInfo")

        configuration = config_loader.find_configuration(MISSION_SUBSCRIPTION_LIST)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"MissionInfo": MissionInfo, "MissionSubscription": MissionSubscription, "MissionRole": MissionRole})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        model_object = response.get_value("model_object")

        return model_object
    
    def creation_mission_subscription(self, config_loader, *args, **kwargs) -> MissionSubscription:
        """return the domain object used to show all the subscriptions in a mission"""
        self.request.set_value("object_class_name", "MissionSubscription")

        configuration = config_loader.find_configuration(MISSION_SUBSCRIPTION)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"MissionSubscription": MissionSubscription, "MissionRole": MissionRole})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        model_object = response.get_value("model_object")

        return model_object
    
    def create_mission_content(self, config_loader, *args, **kwargs) -> MissionContent:
        """return the domain object used a content entry in a mission"""
        self.request.set_value("object_class_name", "MissionContent")

        configuration = config_loader.find_configuration(MISSION_CONTENT)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"MissionContent": MissionContent, "MissionContentData": MissionContentData})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        model_object = response.get_value("model_object")

        return model_object
    
    def create_log(self, config_loader, *args, **kwargs) -> MissionLog:
        """return the domain object used a log entry in a mission"""
        self.request.set_value("object_class_name", "MissionLog")

        configuration = config_loader.find_configuration(MISSION_LOG)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"MissionLog": MissionLog})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        model_object = response.get_value("model_object")

        return model_object
    
    def create_log_collection(self, config_loader, *args, **kwargs) -> MissionInfo:
        self.request.set_value("object_class_name", "MissionInfo")
        
        configuration = config_loader.find_configuration(MISSION_LOG_COLLECTION)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"MissionInfo": MissionInfo, "MissionLog": MissionLog})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")
        
        response = self.execute_sub_action("CreateNode")
        
        model_object = response.get_value("model_object")

        return model_object