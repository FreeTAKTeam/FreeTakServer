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

class ExCheckChecklistController(Controller):
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
        self.template_controller = ExCheckTemplateController(request, response, sync_action_mapper, configuration)
    
    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.template_controller.initialize(request, response)
        self.persistency_controller.initialize(request, response)

    def start_checklist(self, templateuid: str, checklistname: str, checklist_description: str, config_loader, *args, **kwargs):
        """record a new checklist in the component

        Args:
            checklistuid (str): the uid of the new checklist
            checklistdata (str): the content of the checklist
            checklist_description (str): the checklist description
            templateuid (str): the uid of the template from which the template is created
        """
        checklist_uuid = str(uuid.uuid4())

        template = self.template_controller.get_template(templateuid, config_loader)

        parsed_checklist = ElementTree.fromstring(template)

        # parsed_checklist.remove(parsed_checklist.find("checklistColumns"))

        parsed_checklist.find("checklistDetails").find("uid").text = checklist_uuid

        parsed_checklist.find("checklistDetails").find("name").text = checklistname

        parsed_checklist.find("checklistDetails").find("description").text = checklist_description

        try:
            self.persistency_controller.create_checklist(checklist_uuid)
        except Exception:
            pass

        checklist_task_list = self._save_tasks_in_checklist(parsed_checklist)

        self.request.set_value("synctype", "ExCheckChecklist")
        self.request.set_value("objectdata", ElementTree.tostring(parsed_checklist))
        self.request.set_value("objectuid", checklist_uuid)

        self.execute_sub_action("SaveEnterpriseSyncData")

        checklist_tasks = parsed_checklist.find("checklistTasks")

        #for checklist_task in checklist_task_list:
        #    checklist_tasks.append(checklist_task)

        return ElementTree.tostring(parsed_checklist)

    def _save_tasks_in_checklist(self, checklist: Element):
        """
        Retrieve tasks from a checklist and create corresponding checklist tasks.

        Args:
            checklist (Element): The XML element representing the checklist.
        """
        # Extract the UID of the checklist
        checklist_uid = checklist.find("checklistDetails").find("uid").text
        
        # Retrieve the checklist tasks
        checklist_tasks = checklist.find("checklistTasks")
        checklist_task_list = checklist_tasks.findall("checklistTask")
        
        # Iterate over each task in the checklist task list
        for task in checklist_task_list:
            # Create a checklist task using the checklist UID, task UID, and the XML representation of the task
            self.create_checklist_task(checklist_uid, task.find("uid").text, task)

        return checklist_task_list

    def update_checklist_task(self, checklistuid, checklisttaskuid, checklisttaskdata, *args, **kwargs):
        
        self.request.set_value("synctype", "ExCheckChecklistTask")
        self.request.set_value("objectdata", checklisttaskdata)
        self.request.set_value("objectuid", checklisttaskuid)
        self.request.set_value("objecthash", str(hashlib.sha256(checklisttaskdata).hexdigest()))
        self.execute_sub_action("UpdateEnterpriseSyncData")

        self.request.set_value("objectuid", checklistuid)
        sub_response = self.execute_sub_action("GetEnterpriseSyncData")
        checklist_data = sub_response.get_value("objectdata")

        tasks = ElementTree.fromstring(checklist_data).find("checklistTasks").findall("checklistTask")

        for task in tasks:
            if task.find("uid").text == checklisttaskuid:
                task = ElementTree.fromstring(checklisttaskdata)
                break

        self.request.set_value("synctype", "ExCheckChecklist")
        self.request.set_value("objectdata", checklist_data)
        self.request.set_value("objectuid", checklistuid)
        self.execute_sub_action("UpdateEnterpriseSyncData")

        return "done"

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

    def get_checklist(self, checklistuid: str, config_loader, *args, **kwargs) -> str:
        """get the contents of a checklist based on its UID

        Args:
            checklistuid (str): the uid of the checklist to be returned

        Returns:
            str: the content of the checklist
        """

        self.request.set_value("objectuid", checklistuid)

        sub_response = self.execute_sub_action("GetEnterpriseSyncData")

        checklist_content = sub_response.get_value("objectdata")

        checklist_db = self.persistency_controller.get_checklist(checklistuid)

        # task_uids = []
        # for task in checklist_db.tasks:
        #     task_uids.append(task.PrimaryKey)
        
        # self.request.set_value("objectuids", task_uids)

        # sub_response = self.execute_sub_action("GetMultipleEnterpriseSyncData")

        # task_files = sub_response.get_value("objectdata")

        # checklist_with_tasks = self._add_tasks_to_checklist(checklist_content, task_files)

        return ElementTree.tostring(checklist_content)

    def get_all_checklists(self, config_loader, logger, *args, **kwargs):

        checklists = self.persistency_controller.get_all_checklists()

        checklist_uids = [checklist.PrimaryKey for checklist in checklists]

        self.request.set_value("objectuids", checklist_uids)

        sub_response = self.execute_sub_action("GetMultipleEnterpriseSyncData")

        checklist_contents = sub_response.get_value("objectdata")

        complete_checklists = Element("checklists")

        for checklist, checklist_content in zip(checklists, checklist_contents):
            try:
                complete_checklists.append(etree.fromstring(checklist_content))
            except Exception as ex:
                logger.error("error adding checklist to checklist content: %s", ex)
        return ElementTree.tostring(complete_checklists).replace(b"\n", b"")

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

    def _add_tasks_to_checklist(self, checklist: str, tasks: List[str]) -> Element:
        """
        Add tasks to a template XML.

        Args:
            template (str): The template XML as a string.
            tasks (List[str]): A list of task XML strings to be added to the template.
        """

        template_elem = etree.fromstring(checklist)
        template_tasks = template_elem.find("checklistTasks")

        for task in tasks:
            task_elem = etree.fromstring(task)
            task_elem.find("status").text = task_elem.find("status").text.upper()
            template_tasks.append(task_elem)

        return template_elem
    
    def create_checklist_task(self, checklistuid, taskuid, taskdata: Element, *args, **kwargs):
        """create a new template task in the db and the file system"""
        
        # in atak template tasks have no uid so one must be created artificially
        if taskuid is None:
            taskuid = str(uuid.uuid4())
        taskdata.find("status").text = taskdata.find("status").text.upper()
        taskdata.find("uid").text = taskuid
        
        self.request.set_value("synctype", "ExCheckChecklistTask")
        self.request.set_value("objectdata", ElementTree.tostring(taskdata))
        self.request.set_value("objectuid", taskuid)

        self.execute_sub_action("SaveEnterpriseSyncData")

        self.persistency_controller.create_checklist_task(checklistuid, taskuid)