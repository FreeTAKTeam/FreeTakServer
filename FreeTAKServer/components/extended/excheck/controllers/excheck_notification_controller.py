from typing import List
import uuid
from FreeTAKServer.components.extended.excheck.controllers.excheck_template_controller import ExCheckTemplateController
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

from ..domain.mission import Mission
from ..domain.mission_changes import MissionChanges
from ..domain.mission_change import MissionChange
from ..domain.content_resource import ContentResource
from ..domain.creator_uid import CreatorUid
from ..domain.type import Type
from ..domain.submitter import Submitter
from ..domain.mission_name import MissionName
from ..domain.timestamp import Timestamp
from ..domain.uid import Uid
from ..domain.tool import Tool
from ..domain.filename import Filename
from ..domain.hash import Hash
from ..domain.mime_type import MimeType
from ..domain.name import Name
from ..domain.keywords import Keywords
from ..domain.size import Size
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
        checklist = etree.fromstring(self.excheck_checklist_controller.get_checklist(task_uid, config_loader))
        checklist_task = etree.fromstring(self.excheck_checklist_controller.get_checklist_task(task_uid))
        update_task_model_object = self.get_update_task_model_object(config_loader)
        self.complete_update_task_model_object(checklist.find("checklistDetails").find("uid").text, changer_uid, task_uid, task_size, checklist_hash, update_task_model_object)
        # Serializer called by service manager requires the message value
        self.response.set_value('message', [update_task_model_object])
        self.response.set_value('recipients', "*")
        self.response.set_action("publish")

    def get_update_task_model_object(self, config_loader):
        self.request.set_value("object_class_name", EVENT)

        configuration = config_loader.find_configuration(CHECKLIST_UPDATE)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"Mission": Mission, "MissionChanges": MissionChanges, "MissionChange": MissionChange, 
                                                   "contentResource": ContentResource, "creatorUid": CreatorUid, "type": Type, 
                                                   "submitter": Submitter, "missionName": MissionName, "timestamp": Timestamp,
                                                   "uid": Uid, "tool": Tool, "filename": Filename, "hash": Hash, "keywords": Keywords,
                                                   "mimeType": MimeType, "name": Name, "size": Size, "submissionTime": SubmissionTime})
        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")

    def complete_update_task_model_object(self, checklist_uid, changer_uid, task_uid, task_size, checklist_hash, update_task_model_object):
        update_task_model_object.detail.mission.settype("CHANGE")
        update_task_model_object.detail.mission.settool("ExCheck")
        update_task_model_object.detail.mission.setname(checklist_uid)
        update_task_model_object.detail.mission.setauthorUid(changer_uid)
        update_task_model_object.detail.mission.MissionChanges.MissionChange.creatorUid.text = changer_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange.missionName.text = checklist_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange.type.text = "ADD_CONTENT"
        update_task_model_object.detail.mission.MissionChanges.MissionChange.contentResource.filename.text = task_uid + '.xml'
        update_task_model_object.detail.mission.MissionChanges.MissionChange.contentResource.hash.text = checklist_hash
        update_task_model_object.detail.mission.MissionChanges.MissionChange.contentResource.keywords.text = 'Task'
        update_task_model_object.detail.mission.MissionChanges.MissionChange.contentResource.name.text = task_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange.contentResource.size.text = task_size
        # TODO: change this value
        update_task_model_object.detail.mission.MissionChanges.MissionChange.contentResource.submitter.text = 'atak'
        update_task_model_object.detail.mission.MissionChanges.MissionChange.contentResource.uid.text = task_uid