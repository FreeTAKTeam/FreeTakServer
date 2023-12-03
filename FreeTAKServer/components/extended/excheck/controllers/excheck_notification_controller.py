from typing import List
import uuid

from bitarray import bitarray
from FreeTAKServer.components.extended.excheck.controllers.excheck_checklist_controller import ExCheckChecklistController
from FreeTAKServer.components.extended.excheck.controllers.excheck_xml_controller import ExCheckXMLController
from FreeTAKServer.components.extended.excheck.controllers.excheck_domain_controller import ExcheckDomainController
from FreeTAKServer.components.extended.excheck.controllers.excheck_template_controller import ExCheckTemplateController
from FreeTAKServer.components.extended.excheck.domain.content import content
from FreeTAKServer.components.extended.excheck.domain.expiration import expiration
from FreeTAKServer.components.extended.excheck.domain.is_federated_change import isFederatedChange
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from defusedxml import ElementTree

import hashlib

from lxml import etree

from FreeTAKServer.core.configuration.MainConfig import MainConfig

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
from ..domain.submission_time import submissionTime
from ..domain.group_vector import groupVector

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
        self.domain_controller = ExcheckDomainController(request, response, sync_action_mapper, configuration)
        self.xml_controller = ExCheckXMLController(request, response, sync_action_mapper, configuration)

    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.excheck_checklist_controller.initialize(request, response)
        self.persistence_controller.initialize(request, response)
        self.domain_controller.initialize(request, response)
        self.xml_controller.initialize(request, response)

    def generate_group_vector(self):
        length = 32768

        # Create an empty bitarray of the specified length
        bitstring = bitarray(length)

        # Set all bits to 0
        bitstring.setall(False)

        # Set third bit to 1 indicating anonymous group
        bitstring[-3] = True

        # Convert the bitarray to a string representation
        return bitstring.to01()

    def send_task_update_notification(self, task_uid, changer_uid, config_loader, *args, **kwargs):
        checklist_task_obj = self.persistence_controller.get_checklist_task(task_uid)

        self.request.set_value("objectuid", task_uid)

        sub_response = self.execute_sub_action("GetEnterpriseSyncMetaData")
        checklist_task_metadata = sub_response.get_value("objectmetadata")
        
        sub_response = self.execute_sub_action("GetEnterpriseSyncData")
        checklist_task = sub_response.get_value("objectdata")

        self.request.set_value("objectuid", checklist_task_obj.checklist_uid)

        sub_response = self.execute_sub_action("GetEnterpriseSyncData")
        checklist_data = sub_response.get_value("objectdata")

        checklist_element = etree.fromstring(checklist_data)
        
        update_task_model_object = self.domain_controller.get_update_task_model_object(config_loader)
        
        self.complete_update_task_model_object(checklist_task_obj.checklist_uid, changer_uid, task_uid, str(len(checklist_task)), checklist_task_metadata.hash, update_task_model_object, checklist_task)
        
        url = config.DataPackageServiceDefaultIP+":"+str(config.HTTPSTakAPIPort)

        task_data = None
        for task in checklist_element.findall("checklistTasks")[0].findall("checklistTask"):
            if task.find("uid").text == task_uid:
                task_data = task
                break
        
        if task_data.find("status").text == "Complete":
            notes = self.xml_controller.calculate_external_data_update_notes(task_data, checklist_element, changer_uid)  # noqa

            checklist_db = self.persistence_controller.get_checklist_task(task_uid).checklist

            for mission in checklist_db.missions:
                self.request.set_value("mission_id", mission.mission_uid)
                self.request.set_value("external_data_id", checklist_db.PrimaryKey)
                self.request.set_value("notes", notes)
                self.request.set_context("mission")
                ret_topics = self.execute_sub_action("SendExternalDataUpdateNotification").get_value("topics")
                if ret_topics is not None:
                    if self.response.get_value("topics") is None:
                        self.response.set_value("topics", [])
                        self.response.get_value("topics").extend(ret_topics)
                        
        #notification_string = self.sample_notification(checklist_task_metadata.hash, update_task_model_object.stale, task_uid, update_task_model_object.start, len(checklist_task), checklist_task_obj.checklist_uid, checklist_element.find("checklistDetails").find("name").text, url, checklist_task)

        # Serializer called by service manager requires the message value
        self.response.set_value('message', [update_task_model_object])
        #self.response.set_value('message', [notification_string.encode()])
        
        self.response.set_value('recipients', "*")
        self.response.set_action("publish")

    def sample_notification(self, hash, stale_time, task_uid, current_time, task_size, checklist_uid, checklist_name, url, checklist_task):
        from datetime import datetime as dt
        import datetime
        uid_msg = str(uuid.uuid4())
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        timer = dt
        now = timer.utcnow()
        zulu = now.strftime(DATETIME_FMT)
        time_stamp = dt.strptime(zulu, DATETIME_FMT)
        time_str = time_stamp.strftime(DATETIME_FMT)
        add = datetime.timedelta(seconds=20)
        stale_part = dt.strptime(zulu, DATETIME_FMT) + add
        stale = stale_part.strftime(DATETIME_FMT)
        from jinja2 import Environment, FileSystemLoader

        # Create a Jinja environment with the specified template directory
        env = Environment(loader=FileSystemLoader(r"C:\Users\Natha Paquette\work\FreeTakServer\FreeTAKServer\components\extended\excheck\configuration"))
        
        # Load the template file
        template = env.get_template('notification_template.jinja')
        
        # Render the template to a string
        rendered_template = template.render(uid_msg=uid_msg, stale=stale, time_str=time_str, hash=hash, stale_time=stale_time, task_uid=task_uid, current_time=current_time, task_size=task_size+55, checklist_uid=checklist_uid, checklist_name=checklist_name, checklist_task=checklist_task)
        
        print(rendered_template)

        return rendered_template
    
    

    def complete_update_task_model_object(self, checklist_uid, changer_uid, task_uid, task_size, checklist_hash, update_task_model_object, task_data):
        update_task_model_object.type = "t-x-m-c"
        update_task_model_object.version = "2.0"
        update_task_model_object.how = "h-g-i-g-o"
        update_task_model_object.uid = str(uuid.uuid4())
        update_task_model_object.point.hae = "0"
        update_task_model_object.detail.mission.type = "CHANGE"
        update_task_model_object.detail.mission.tool = "ExCheck"
        update_task_model_object.detail.mission.name = checklist_uid
        update_task_model_object.detail.mission.authorUid = changer_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].creatorUid.text = changer_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].isFederatedChange.text = 'false'
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].missionName.text = checklist_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].timestamp.text = update_task_model_object.start
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].type.text = "ADD_CONTENT"

        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.filename.text = task_uid + '.xml'
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.hash.text = checklist_hash
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.keywords.text = 'Task'
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.mimeType.text = 'application/xml'
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.name.text = task_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.size.text = task_size
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.submissionTime.text = update_task_model_object.start
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.submitter.text = "anonymous"
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.tool.text = "ExCheck"
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.uid.text = task_uid
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.expiration.text = "-1"
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].contentResource.groupVector.text = self.generate_group_vector()

        # TODO: change this value
        update_task_model_object.detail.mission.MissionChanges.MissionChange[0].content.text = task_data
        
    def serialize_model_object(self, model_object):
        self.request.set_value("protocol", "xml")
        self.request.set_value("message", [model_object])
        response = self.execute_sub_action("serialize")
        # add the serialized model object to the controller response as a value
        return response.get_value("message")