from typing import List
import uuid
from FreeTAKServer.components.extended.excheck.controllers.excheck_template_controller import ExCheckTemplateController
from FreeTAKServer.components.extended.excheck.domain.content import content
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from defusedxml import ElementTree

import hashlib

from lxml.etree import Element
from lxml import etree

from FreeTAKServer.core.configuration.MainConfig import MainConfig

from .excheck_checklist_controller import ExCheckChecklistController
from .excheck_persistency_controller import ExCheckPersistencyController

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
from ..domain.submission_time import SubmissionTime

from ..configuration.excheck_constants import (
    BASE_OBJECT,
    BASE_OBJECT_NAME,
    CHECKLIST_UPDATE,
    EVENT
)

config = MainConfig.instance()

class ExCheckNotificationController(Controller):
    """manage notifications"""
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, sync_action_mapper, configuration)
        self.excheck_checklist_controller = ExCheckChecklistController(request, response, sync_action_mapper, configuration)
        self.persistence_controller = ExCheckPersistencyController(request, response, sync_action_mapper, configuration)
    
    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.excheck_checklist_controller.initialize(request, response)
        self.persistence_controller.initialize(request, response)

    def send_task_update_notification(self, task_uid, changer_uid, config_loader, *args, **kwargs):
        checklist_task_obj = self.persistence_controller.get_checklist_task(task_uid)
        
        self.request.set_value("objectuid", task_uid)

        sub_response = self.execute_sub_action("GetEnterpriseSyncMetaData")
        checklist_task_metadata = sub_response.get_value("objectmetadata")
        
        sub_response = self.execute_sub_action("GetEnterpriseSyncData")
        checklist_task = sub_response.get_value("objectdata")
        
        update_task_model_object = self.get_update_task_model_object(config_loader)
        
        self.complete_update_task_model_object(checklist_task_obj.checklist_uid, changer_uid, task_uid, str(len(checklist_task)), checklist_task_metadata.hash, update_task_model_object, checklist_task)
        
        #serialized_object = self.serialize_model_object(update_task_model_object)

        # Serializer called by service manager requires the message value
        self.response.set_value('message', [update_task_model_object])
        self.response.set_value('recipients', "*")
        self.response.set_action("publish")

    def get_update_task_model_object(self, config_loader):
        self.request.set_value("object_class_name", EVENT)

        configuration = config_loader.find_configuration(CHECKLIST_UPDATE)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"mission": mission, "MissionChanges": MissionChanges, "MissionChange": MissionChange, 
                                                   "contentResource": contentResource, "creatorUid": creatorUid, "type": type, 
                                                   "submitter": submitter, "missionName": missionName, "timestamp": timestamp,
                                                   "uid": uid, "tool": tool, "filename": filename, "hash": hash, "keywords": keywords,
                                                   "mimeType": mimeType, "name": name, "size": size, "submissionTime": SubmissionTime,
                                                   "content": content})
        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")

    def complete_update_task_model_object(self, checklist_uid, changer_uid, task_uid, task_size, checklist_hash, update_task_model_object, task_data):
        update_task_model_object.type = "t-x-m-c"
        update_task_model_object.version = "2.0"
        update_task_model_object.how = "m-g"
        update_task_model_object.uid = str(uuid.uuid4())
        update_task_model_object.detail.mission.type = "CHANGE"
        update_task_model_object.detail.mission.tool = "ExCheck"
        update_task_model_object.detail.mission.name = checklist_uid
        update_task_model_object.detail.mission.authorUid = changer_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].creatorUid.text = changer_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].missionName.text = checklist_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].type.text = "CHANGE"
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.filename.text = task_uid + '.xml'
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.hash.text = checklist_hash
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.keywords.text = 'Task'
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.name.text = task_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.size.text = task_size
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.tool.text = "ExCheck"
        # TODO: change this value
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.submitter.text = 'atak'
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.uid.text = task_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].content.text = task_data
        
    def serialize_model_object(self, model_object):
        self.request.set_value("protocol", "xml")
        self.request.set_value("message", [model_object])
        response = self.execute_sub_action("serialize")
        # add the serialized model object to the controller response as a value
        return response.get_value("message")