from typing import List
import uuid
from FreeTAKServer.components.extended.excheck.controllers.excheck_domain_controller import ExcheckDomainController
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from defusedxml import ElementTree

import hashlib

from lxml import etree


from FreeTAKServer.core.configuration.MainConfig import MainConfig

from FreeTAKServer.components.core.fts_domain.domain import MissionInfo
from FreeTAKServer.components.core.fts_domain.domain import MissionData
from FreeTAKServer.components.core.fts_domain.domain import MissionContent
from FreeTAKServer.components.core.fts_domain.domain import MissionContentData

from .excheck_persistency_controller import ExCheckPersistencyController

from ..configuration.excheck_constants import (
    BASE_OBJECT,
    BASE_OBJECT_NAME,
    TEMPLATE_CONTENT,
    TEMPLATE_METADATA
)

config = MainConfig.instance()

class ExCheckMissionController(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, sync_action_mapper, configuration)
        self.persistency_controller = ExCheckPersistencyController(request, response, sync_action_mapper, configuration)
        self.domain_controller = ExcheckDomainController(request, response, sync_action_mapper, configuration)

    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.persistency_controller.initialize(request, response)
        self.domain_controller.initialize(request, response)

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
        mission_item_metadata_list: List[MissionContent]= mission_data.contents
        if len(mission_item_metadata_list)>0:
            self._serialize_template_metadata(mission_item_metadata_list[0], object_metadata[0])
            for index in range(1, len(object_metadata)):
                mission_item_metadata: MissionContentData = self.domain_controller.get_mission_item_metadata_object(config_loader)
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
