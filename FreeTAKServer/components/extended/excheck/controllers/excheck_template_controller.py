from typing import List
import uuid
from xml.etree.ElementTree import Element
from FreeTAKServer.components.extended.excheck.controllers.excheck_domain_controller import ExcheckDomainController
from FreeTAKServer.core.util.time_utils import get_current_dtg
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from defusedxml import ElementTree

import hashlib

from lxml import etree

from lxml.etree import Element as lxmlElement

from datetime import datetime as dt

from FreeTAKServer.core.configuration.MainConfig import MainConfig

from FreeTAKServer.components.core.domain.domain import MissionInfo
from FreeTAKServer.components.core.domain.domain import MissionData
from FreeTAKServer.components.core.domain.domain import MissionContentData
from FreeTAKServer.components.core.domain.domain import MissionContent

from .excheck_persistency_controller import ExCheckPersistencyController

from ..configuration.excheck_constants import (
    BASE_OBJECT,
    BASE_OBJECT_NAME,
    TEMPLATE_CONTENT,
    TEMPLATE_METADATA
)

DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

config = MainConfig.instance()

class ExCheckTemplateController(Controller):
    """manage template operations"""
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

    def create_template_mission(self):
        """create a new mission for the templates"""
        self.request.set_value("mission_id", "exchecktemplates")
        self.request.set_value("mission_data", b"")
        self.request.set_value("mission_data_args",  {
            'defaultRole': "MISSION_OWNER",
            'tool': "ExCheck",
            'downloaded': False,
            'connected': True,
            'isSubscribed': True,
            'autoPublish': False,
            'description': "",
            'uids': [],
            'contents': [],
            'createTime': get_current_dtg(),
            'passwordProtected': False,
            'groups': [],
            'serviceUri': ''})
        self.request.set_value("creatorUid", "ExCheck")
        self.request.set_context("mission")
        self.execute_sub_action("PutMission")

    def create_template(self, templatedata: str, creator_uid:str, *args, **kwargs):
        """record a new template in the component

        Args:
            templateuid (str): the uid of the new template
            templatedata (str): the content of the template
        """
        parsed_template = etree.fromstring(templatedata)
        
        template_uid = parsed_template.find("checklistDetails").find("uid").text
        try:
            self.persistency_controller.create_template(template_uid)
        except Exception:
            pass

        for checklist_task in parsed_template.find("checklistTasks").findall("checklistTask"):
            if checklist_task.find("number") == None:
                num_elem = lxmlElement("number")
                num_elem.text = b'0'
                checklist_task.append(num_elem)

        self.request.set_value("synctype", "ExCheckTemplate")
        self.request.set_value("objecthash", str(hashlib.sha256(templatedata).hexdigest()))
        self.request.set_value("objectdata", ElementTree.tostring(parsed_template))
        self.request.set_value("objectuid", template_uid)
        self.request.set_value("objkeywords", [parsed_template.find("checklistDetails").find("name").text,
                                                parsed_template.find("checklistDetails").find("description").text,
                                                parsed_template.find("checklistDetails").find("creatorCallsign").text])
        self.request.set_value("tool", "ExCheck")
        self.request.set_value("creator_uid", creator_uid)
        self.request.set_value("mime_type", "application/xml")        
        self.request.set_value("objstarttime", self.get_time())

        save_metadata = self.execute_sub_action("SaveEnterpriseSyncData").get_value("objectmetadata")

        self.request.set_value("mission_id", "exchecktemplates")

        self.request.set_value("hashes", [save_metadata.hash])

        self.request.set_context("mission")

        self.execute_sub_action("AddMissionContents")

    def get_template(self, templateuid: str, config_loader, *args, **kwargs) -> str:
        """get the contents of a template based on its UID

        Args:
            templateuid (str): the uid of the template to be returned

        Returns:
            str: the content of the template
        """

        self.request.set_value("objectuid", templateuid)

        sub_response = self.execute_sub_action("GetEnterpriseSyncData")

        template_content = sub_response.get_value("objectdata")
        
        self.response.set_value("template_data", template_content)

        return template_content

    def get_all_templates(self, config_loader, logger, *args, **kwargs):

        templates = self.persistency_controller.get_all_templates()

        template_uids = [template.PrimaryKey for template in templates]

        self.request.set_value("objectuids", template_uids)

        sub_response = self.execute_sub_action("GetMultipleEnterpriseSyncMetaData")

        template_metadata = sub_response.get_value("objectmetadata")

        self.request.set_value("use_bytes", True)

        sub_response = self.execute_sub_action("GetMultipleEnterpriseSyncData")

        template_contents = sub_response.get_value("objectdata")

        complete_templates = []

        template_lengths = []

        for template, template_content in zip(templates, template_contents):
            try:
                complete_templates.append(etree.fromstring(template_content))
                template_lengths.append(len(template_content))
            except Exception as ex:
                logger.error("error adding template \n template: %s exception: %s", template, ex)
        
        mission_info = self.domain_controller.get_mission_info_object(config_loader)

        self._serialize_to_mission_info(mission_info, complete_templates, template_metadata, config_loader, template_lengths)

        final_message = self._serialize_to_json(mission_info)

        self.response.set_value("template_info", final_message[0])

        return final_message[0]
    
    def get_time(self):
        timer = dt
        now = timer.utcnow()
        return now.strftime(DATETIME_FMT)


    def _serialize_to_json(self, message):
        self.request.set_value("protocol", "json")
        self.request.set_value("message", [message])
        response = self.execute_sub_action("serialize")
        return response.get_value("message")

    def _serialize_to_mission_info(self, mission_info: MissionInfo, templates: List[Element], template_metadata: List, config_loader, template_lengths):
        #TODO: modify this to access from the configuration
        mission_info.nodeId = config.nodeID
        #mission_info.nodeId = "b9a1620a93ec43378f42a32103f53d8d"
        mission_info.version = config.APIVersion
        mission_info.type = "Mission"
        mission_data: List[MissionData] = mission_info.data[0] # the only mission data object should be the excheck object
        self._serialize_to_mission_data(mission_data, templates, template_metadata, config_loader, template_lengths)

    def _serialize_to_mission_data(self, mission_data, templates, template_metadata_objs, config_loader, template_lengths):
        mission_data.name = "exchecktemplates"
        mission_data.tool = "ExCheck"
        mission_data.keywords = []
        mission_data.creatorUid = "ExCheck"
        # TODO: get time dynamically
        mission_data.createTime = "2023-02-22T16:06:26.979Z"
        mission_data.groups = []
        mission_data.feeds = []
        mission_data.mapLayers = []
        mission_data.inviteOnly = False
        mission_data.expiration = -1
        mission_data.uids = []
        mission_data.passwordProtected = False
        template_metadata_list: List[MissionContent]= mission_data.contents
        if len(template_metadata_list)>0 and len(templates)>0:
            self._serialize_template_metadata(template_metadata_list[0], templates[0], template_metadata_objs[0], template_lengths[0])
            for index in range(1, len(templates)):
                template_metadata: MissionContent = self.domain_controller.get_template_metadata_object(config_loader)
                mission_data.contents = template_metadata
                self._serialize_template_metadata(template_metadata, templates[index], template_metadata_objs[index], template_lengths[index])

    def _serialize_template_metadata(self, template_metadata, template, template_metadata_obj, template_len):
        template_str = etree.tostring(template, encoding='UTF-8', method='xml', standalone="yes")
        template_metadata.creatorUid = "ANDROID-860046038899730"
        template_metadata.timestamp = "2023-02-23T18:46:46.554Z"

        self._serialize_template_content(template, template_str, template_metadata, template_metadata_obj, template_len)

    def _serialize_template_content(self, template, template_str, template_metadata, template_metadata_obj, template_len):
        template_content: MissionContentData = template_metadata.data
        template_details = template.find("checklistDetails")

        template_content.filename = template_details.find("uid").text+".xml"
        template_content.keywords = [template_details.find("name").text, template_details.find("description").text, "TODO"]
        template_content.mimeType = "application/xml"
        template_content.name = template_details.find("uid").text
        template_content.submissionTime = template_details.find("startTime").text
        template_content.submitter = "TODO"
        template_content.name = template_details.find("uid").text
        template_content.hash = template_metadata_obj.hash
        template_content.size = template_len
        template_content.tool = "ExCheck"
        template_content.uid = template_details.find("uid").text
        template_content.expiration = -1
