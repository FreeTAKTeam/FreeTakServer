from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from FreeTAKServer.components.extended.excheck.domain.content import content
from FreeTAKServer.components.extended.excheck.domain.expiration import expiration
from FreeTAKServer.components.extended.excheck.domain.is_federated_change import isFederatedChange
from ..domain.mission import mission
from ..domain.mission_changes import MissionChanges
from ..domain.mission_change import MissionChange
from ..domain.content_resource import contentResource
from ..domain.creator_uid import creatorUid
from ..domain.type import type
from ..domain.submitter import submitter
from ..domain.mission_name import missionName
from ..domain.timestamp import timestamp
from ..domain.uid import uid
from ..domain.tool import tool
from ..domain.filename import filename
from ..domain.hash import hash
from ..domain.mime_type import mimeType
from ..domain.name import name
from ..domain.keywords import keywords
from ..domain.size import size
from ..domain.submission_time import submissionTime
from ..domain.group_vector import groupVector

from ..configuration.excheck_constants import (
    BASE_OBJECT,
    BASE_OBJECT_NAME,
    CHECKLIST_UPDATE,
    EVENT,
    TEMPLATE_CONTENT,
    TEMPLATE_METADATA
)

class ExcheckDomainController(Controller):
    
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, sync_action_mapper, configuration)

    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)

    def get_mission_item_metadata_object(self, config_loader):

        self.request.set_value("object_class_name", "MissionContent")

        configuration = config_loader.find_configuration(TEMPLATE_METADATA)

        self.request.set_value("configuration", configuration)

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")
    
    def get_mission_info_object(self, config_loader, *args, **kwargs):
        self.request.set_value("object_class_name", BASE_OBJECT_NAME)

        configuration = config_loader.find_configuration(TEMPLATE_CONTENT)

        self.request.set_value("configuration", configuration)

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")
    
    def get_update_task_model_object(self, config_loader):
        self.request.set_value("object_class_name", EVENT)

        configuration = config_loader.find_configuration(CHECKLIST_UPDATE)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"mission": mission, "MissionChanges": MissionChanges, "MissionChange": MissionChange, 
                                                   "contentResource": contentResource, "creatorUid": creatorUid, "type": type, 
                                                   "submitter": submitter, "missionName": missionName, "timestamp": timestamp,
                                                   "uid": uid, "tool": tool, "filename": filename, "hash": hash, "keywords": keywords,
                                                   "mimeType": mimeType, "name": name, "size": size, "submissionTime": submissionTime,
                                                   "content": content, "isFederatedChange": isFederatedChange, "expiration": expiration,
                                                   "groupVector": groupVector})
        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")

    def get_template_metadata_object(self, config_loader):

        self.request.set_value("object_class_name", "MissionItemMetaData")

        configuration = config_loader.find_configuration(TEMPLATE_METADATA)

        self.request.set_value("configuration", configuration)

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")