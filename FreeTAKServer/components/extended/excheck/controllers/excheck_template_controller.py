from typing import List
import uuid
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from defusedxml import ElementTree

import hashlib

from lxml.etree import Element

from FreeTAKServer.core.configuration.MainConfig import MainConfig

from ..domain.mission_info import MissionInfo
from ..domain.mission_data import MissionData
from ..domain.template_content import TemplateContent
from ..domain.template_metadata import TemplateMetaData

from .excheck_persistency_controller import ExCheckPersistencyController

from ..configuration.excheck_constants import (
    BASE_OBJECT,
    BASE_OBJECT_NAME,
    TEMPLATE_CONTENT,
    TEMPLATE_METADATA
)

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

    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.persistency_controller.initialize(request, response)

    def create_template(self, templatedata: str, *args, **kwargs):
        """record a new template in the component

        Args:
            templateuid (str): the uid of the new template
            templatedata (str): the content of the template
        """
        parsed_template = ElementTree.fromstring(templatedata)
        
        template_uid = parsed_template.find("checklistDetails").find("uid").text
        try:
            self.persistency_controller.create_template(template_uid)
        except Exception:
            pass
        self._save_tasks_in_template(parsed_template)

        self.request.set_value("synctype", "ExCheckTemplate")
        self.request.set_value("objectdata", ElementTree.tostring(parsed_template))
        self.request.set_value("objectuid", template_uid)

        self.execute_sub_action("SaveEnterpriseSyncData")

    def _save_tasks_in_template(self, template: Element):
        """
        Retrieve tasks from a template and create corresponding template tasks.

        Args:
            template (Element): The XML element representing the template.
        """
        # Extract the UID of the template
        template_uid = template.find("checklistDetails").find("uid").text
        
        # Retrieve the template tasks
        template_tasks = template.find("checklistTasks")
        template_task_list = template_tasks.findall("checklistTask")
        
        # Iterate over each task in the template task list
        for task in template_task_list:
            # Create a template task using the template UID, task UID, and the XML representation of the task
            self.create_template_task(template_uid, task.find("uid").text, ElementTree.tostring(task))
        
        # Remove the tasks from the template
        for task in template_task_list:
            template_tasks.remove(task)

    def get_mission_info_object(self, config_loader):
       
        self.request.set_value("object_class_name", BASE_OBJECT_NAME)

        configuration = config_loader.find_configuration(TEMPLATE_CONTENT)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"MissionData": MissionData, "MissionInfo": MissionInfo, "TemplateMetaData": TemplateMetaData, "TemplateContent": TemplateContent})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")

    def get_template_metadata_object(self, config_loader):

        self.request.set_value("object_class_name", "TemplateMetaData")

        configuration = config_loader.find_configuration(TEMPLATE_METADATA)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"TemplateMetaData": TemplateMetaData, "TemplateContent": TemplateContent})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        return response.get_value("model_object")

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

        template_db = self.persistency_controller.get_template(templateuid)

        task_uids = []
        for task in template_db.tasks:
            task_uids.append(task.PrimaryKey)
        
        self.request.set_value("objectuids", task_uids)

        sub_response = self.execute_sub_action("GetMultipleEnterpriseSyncData")

        task_files = sub_response.get_value("objectdata")

        template_with_tasks = self._add_tasks_to_template(template_content, task_files)

        return ElementTree.tostring(template_with_tasks)

    def get_all_templates(self, config_loader, *args, **kwargs):

        templates = self.persistency_controller.get_all_templates()

        template_uids = [template.PrimaryKey for template in templates]

        self.request.set_value("objectuids", template_uids)

        sub_response = self.execute_sub_action("GetMultipleEnterpriseSyncData")

        template_contents = sub_response.get_value("objectdata")

        complete_templates = []

        for template, template_content in zip(templates, template_contents):
            task_uids = []
            for task in template.tasks:
                task_uids.append(task.PrimaryKey)

            self.request.set_value("objectuids", task_uids)

            sub_response = self.execute_sub_action("GetMultipleEnterpriseSyncData")

            task_files = sub_response.get_value("objectdata")

            template_with_tasks = self._add_tasks_to_template(template_content, task_files)

            complete_templates.append(template_with_tasks)

        mission_info = self.get_mission_info_object(config_loader)

        self._serialize_to_mission_info(mission_info, complete_templates, config_loader)

        final_message = self._serialize_to_json(mission_info)

        return final_message[0]

    def _serialize_to_json(self, message):
        self.request.set_value("protocol", "json")
        self.request.set_value("message", [message])
        response = self.execute_sub_action("serialize")
        return response.get_value("message")

    def _serialize_to_mission_info(self, mission_info: MissionInfo, templates: List[Element], config_loader):
        #TODO: modify this to access from the configuration
        mission_info.nodeId = config.nodeID
        #mission_info.nodeId = "b9a1620a93ec43378f42a32103f53d8d"
        mission_info.version = config.APIVersion
        mission_info.type = "Mission"
        mission_data: List[MissionData] = mission_info.data[0] # the only mission data object should be the excheck object
        self._serialize_to_mission_data(mission_data, templates, config_loader)

    def _serialize_to_mission_data(self, mission_data, templates, config_loader):
        mission_data.name = "exchecktemplates"
        mission_data.tool = "ExCheck"
        mission_data.keywords = []
        mission_data.creatorUid = "ExCheck"
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
        template_metadata_list: List[TemplateMetaData]= mission_data.contents
        if len(template_metadata_list)>0 and len(templates)>0:
            self._serialize_template_metadata(template_metadata_list[0], templates[0])
            for index in range(1, len(templates)):
                template_metadata: TemplateMetaData = self.get_template_metadata_object(config_loader)
                mission_data.contents = template_metadata
                self._serialize_template_metadata(template_metadata, templates[index])

    def _serialize_template_metadata(self, template_metadata, template):
        template_str = ElementTree.tostring(template)
        template_metadata.creatorUid = "ANDROID-860046038899730"
        template_metadata.timestamp = "2023-02-23T18:46:46.554Z"

        self._serialize_template_content(template, template_str, template_metadata)

    def _serialize_template_content(self, template, template_str, template_metadata):
        template_content: TemplateContent = template_metadata.data
        template_details = template.find("checklistDetails")

        template_content.filename = template_details.find("uid").text+".xml"
        template_content.keywords = [template_details.find("name").text, template_details.find("description").text, "TODO"]
        template_content.mimeType = "application/xml"
        template_content.name = template_details.find("uid").text
        template_content.submissionTime = template_details.find("startTime").text
        template_content.submitter = "TODO"
        template_content.name = template_details.find("uid").text
        template_content.hash = str(hashlib.sha256(template_str).hexdigest())
        template_content.size = len(template_str)
        template_content.tool = "ExCheck"
        template_content.uid = template_details.find("uid").text

    def _add_tasks_to_template(self, template: str, tasks: List[str]) -> Element:
        """
        Add tasks to a template XML.

        Args:
            template (str): The template XML as a string.
            tasks (List[str]): A list of task XML strings to be added to the template.
        """

        template_elem = ElementTree.fromstring(template)
        template_tasks = template_elem.find("checklistTasks")

        for task in tasks:
            task_elem = ElementTree.fromstring(task)
            template_tasks.append(task_elem)

        return template_elem
    
    def create_template_task(self, templateuid, taskuid, taskdata, *args, **kwargs):
        """create a new template task in the db and the file system"""
        
        # in atak template tasks have no uid so one must be created artificially
        if taskuid is None:
            taskuid = str(uuid.uuid4())
        
        self.request.set_value("synctype", "ExCheckTemplateTask")
        self.request.set_value("objectdata", taskdata)
        self.request.set_value("objectuid", taskuid)

        self.execute_sub_action("SaveEnterpriseSyncData")

        self.persistency_controller.create_template_task(templateuid, taskuid)