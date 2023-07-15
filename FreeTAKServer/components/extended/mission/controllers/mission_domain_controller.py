from FreeTAKServer.components.core.domain.domain import Event
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
from ..domain.mission_item import MissionItem as DomainMissionItem
from ..domain.mission_item_metadata import MissionItemMetaData as DomainMissionItemMetaData
from ..domain.mission import mission as DomainMissionCot

from ..persistence.mission import Mission as DBMission
from ..persistence.subscription import Subscription as DBSubscription

from ..configuration.mission_constants import (
    BASE_OBJECT_NAME,
    MISSION_CONTENT,
    MISSION_ITEM,
    MISSION_RECORD,
    MISSION_SUBSCRIPTION,
    MISSION_NOTIFICATION,
    MISSION_COLLECTION
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

        self.request.set_value("extended_domain", {"MissionData": MissionData, "MissionItemMetaData": DomainMissionItemMetaData, "MissionItem": DomainMissionItem, "ExternalData": ExternalData, "MissionRole": MissionRole})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")
    
    def complete_mission_record_db(self, mission_domain_object: MissionData, mission_db_object: DBMission, subscription: DBSubscription = None, **kwargs) -> MissionData: # type: ignore
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
    
    def 