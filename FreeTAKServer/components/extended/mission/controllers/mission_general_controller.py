from typing import List
from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import MissionPersistenceController
from FreeTAKServer.components.extended.mission.domain.external_data import ExternalData
from FreeTAKServer.components.extended.mission.domain.mission_role import MissionRole
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from FreeTAKServer.core.configuration.MainConfig import MainConfig

from ..domain.mission_info import MissionInfo
from ..domain.mission_data import MissionData
from ..domain.mission_item import MissionItem
from ..domain.mission_item_metadata import MissionItemMetaData

from ..configuration.mission_constants import (
    BASE_OBJECT_NAME,
    MISSION_CONTENT,
    MISSION_ITEM,
    MISSION_SUBSCRIPTION
)

config = MainConfig.instance()


class MissionGeneralController(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
        ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.persistency_controller = MissionPersistenceController(request, response, sync_action_mapper, configuration)

    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.persistency_controller.initialize(request, response)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
 
    def put_mission(self, mission_id, mission_data, config_loader, *args, **kwargs):
        """this method is used to create a new mission, save it to the database and return the mission information
        to the client in json format, it uses the mission persistence controller to access the database.
        """
        mission_db_obj = self.persistency_controller.create_mission(mission_id, mission_data)
        mission_subscription_obj = self.get_mission_subscription(mission_id, config_loader)
        self.response.set_value("mission_info", self.get_mission(mission_id))
        return self.response

    def get_mission_subscription(self, subscription_obj, config_loader, *args, **kwargs):
        return self.get_mission_subscription_object(config_loader)

    def get_mission(self, mission_id, config_loader, *args, **kwargs):
        """_summary_
        """
        mission_info = self.get_mission_info_object(config_loader)
        checklist_db_obj = self.persistency_controller.get_checklist(mission_id)
        
        mission_uids = [checklist_task.PrimaryKey for checklist_task in checklist_db_obj.tasks]
        self.request.set_value("objectuids", mission_uids)
        sub_resp = self.execute_sub_action("GetMultipleEnterpriseSyncMetaData")

        mission_elements_metadata = sub_resp.get_value("objectmetadata")

        self.complete_mission_info(mission_info, mission_elements_metadata, mission_id, config_loader)

        final_message = self.serialize_to_json(mission_info)
        
        self.response.set_value("mission_info", final_message[0])
        
        return final_message[0]

    def serialize_mission(self, **kwargs):
        """this is the general method used to serialize the component to a given format"""
        # serialize the component model object in a sub-action
        response = self.execute_sub_action(
        self.request.get_value("model_object_parser")
        )
        # add the serialized model object to the controller response as a value
        self.response.set_value(
        "serialized_message", response.get_value("serialized_message")
        )
        self.request.get_value("logger").debug(
        "serialized component message to format "
        + self.request.get_value("model_object_parser")
        )

    def get_mission_info_object(self, config_loader, *args, **kwargs):
        self.request.set_value("object_class_name", BASE_OBJECT_NAME)

        configuration = config_loader.find_configuration(MISSION_CONTENT)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"MissionData": MissionData, "MissionInfo": MissionInfo, "MissionItemMetaData": MissionItemMetaData, "MissionItem": MissionItem})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")
    
    def get_mission_subscription_object(self, config_loader, *args, **kwargs):
        """create a new mission subscription object"""
        self.request.set_value("object_class_name", BASE_OBJECT_NAME)

        configuration = config_loader.find_configuration(MISSION_SUBSCRIPTION)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"MissionData": MissionData, "MissionInfo": MissionInfo, "MissionItemMetaData": MissionItemMetaData, "MissionItem": MissionItem, "MissionRoleDefault": MissionRole, "MissionRoleOwner": MissionRole, "ExternalData": ExternalData})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")
    
    def get_mission_item_metadata_object(self, config_loader):

        self.request.set_value("object_class_name", "MissionItemMetaData")

        configuration = config_loader.find_configuration(MISSION_ITEM)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"MissionItemMetaData": MissionItemMetaData, "MissionItem": MissionItem})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")
    
    def complete_mission_info(self, mission_info: MissionInfo, object_metadata: List, mission_id: str, config_loader):
        mission_info.nodeId = config.nodeID
        mission_info.version = config.APIVersion
        mission_info.type = "Mission"
        mission_data: List[MissionData] = mission_info.data[0] # the only mission data object should be the excheck object
        self._serialize_to_mission_data(mission_data, object_metadata, mission_id, config_loader)

    def _serialize_to_mission_data(self, mission_data, object_metadata, mission_id, config_loader):
        mission_data.name = mission_id
        mission_data.description = ""
        mission_data.chatRoom = ""
        mission_data.baseLayer = ""
        mission_data.bbox = ""
        mission_data.path = ""
        mission_data.classification = ""
        mission_data.tool = "ExCheck"
        mission_data.keywords = []
        mission_data.creatorUid = ""
        # TODO: get time dynamically
        mission_data.createTime = "2023-02-22T16:06:26.979Z"
        mission_data.groups = []
        mission_data.externalData = []
        mission_data.feeds = []
        mission_data.mapLayers = []
        mission_data.inviteOnly = False
        mission_data.expiration = -1
        mission_data.uids = []
        mission_data.passwordProtected = False
        mission_item_metadata_list: List[MissionItemMetaData]= mission_data.contents
        if len(mission_item_metadata_list)>0:
            self._serialize_template_metadata(mission_item_metadata_list[0], object_metadata[0])
            for index in range(1, len(object_metadata)):
                mission_item_metadata: MissionItemMetaData = self.get_mission_item_metadata_object(config_loader)
                mission_data.contents = mission_item_metadata
                self._serialize_template_metadata(mission_item_metadata, object_metadata[index])

    def _serialize_template_metadata(self, mission_item_metadata, object_metadata):
        mission_item_metadata.creatorUid = object_metadata.creator_uid
        mission_item_metadata.timestamp = object_metadata.start_time

        self._serialize_template_content(mission_item_metadata.data, object_metadata)

    def _serialize_template_content(self, mission_item, mission_item_entry):

        mission_item.filename = mission_item_entry.PrimaryKey+".xml"
        keywords = []
        for keyword in mission_item_entry.keywords:
            keywords.append(keyword.keyword)
        mission_item.keywords = keywords
        mission_item.mimeType = mission_item_entry.mime_type
        mission_item.name = mission_item_entry.PrimaryKey
        mission_item.submissionTime = mission_item_entry.start_time
        mission_item.submitter = mission_item_entry.submitter
        mission_item.name = mission_item_entry.PrimaryKey
        mission_item.hash = mission_item_entry.hash
        mission_item.size = mission_item_entry.length
        mission_item.tool = mission_item_entry.tool
        mission_item.uid = mission_item_entry.PrimaryKey
        mission_item.expiration = mission_item_entry.expiration

    def serialize_to_json(self, message):
        self.request.set_value("protocol", "json")
        self.request.set_value("message", [message])
        response = self.execute_sub_action("serialize")
        return response.get_value("message")
