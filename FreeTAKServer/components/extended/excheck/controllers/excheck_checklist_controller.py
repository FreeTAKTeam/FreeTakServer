from typing import List
import uuid
from FreeTAKServer.components.extended.excheck.controllers.excheck_domain_controller import ExcheckDomainController
from FreeTAKServer.components.extended.excheck.controllers.excheck_template_controller import ExCheckTemplateController
from FreeTAKServer.components.extended.excheck.controllers.excheck_wintak_adapter import ExCheckWintakAdapter
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from bitarray import bitarray

from defusedxml import ElementTree

import hashlib

from datetime import datetime as dt

from xml.etree.ElementTree import Element as etElement

from lxml.etree import Element
from lxml import etree

from FreeTAKServer.core.configuration.MainConfig import MainConfig

from .excheck_persistency_controller import ExCheckPersistencyController
from .excheck_mission_controller import ExCheckMissionController

from ..configuration.excheck_constants import (
    BASE_OBJECT,
    BASE_OBJECT_NAME,
    TEMPLATE_CONTENT,
    TEMPLATE_METADATA
)

DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

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
        self.wintak_adapter = ExCheckWintakAdapter(request, response, sync_action_mapper, configuration)
        self.mission_controller = ExCheckMissionController(request, response, sync_action_mapper, configuration)
        self.domain_controller = ExcheckDomainController(request, response, sync_action_mapper, configuration)

    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.template_controller.initialize(request, response)
        self.persistency_controller.initialize(request, response)
        self.wintak_adapter.initialize(request, response)
        self.mission_controller.initialize(request, response)
        self.domain_controller.initialize(request, response)

    def start_checklist(self, templateuid: str, checklistname: str, checklist_description: str,  config_loader, checklist_content: bytes=b"", *args, **kwargs):
        """record a new checklist in the component

        Args:
            checklistuid (str): the uid of the new checklist
            checklistdata (str): the content of the checklist
            checklist_description (str): the checklist description
            templateuid (str): the uid of the template from which the template is created
        """
        if checklist_content == b'':
            start_time = self.get_time()
            
            checklist_uuid = str(uuid.uuid4())

            template = self.template_controller.get_template(templateuid, config_loader)

            parsed_checklist = etree.fromstring(template)

            # parsed_checklist.remove(parsed_checklist.find("checklistColumns"))

            parsed_checklist.find("checklistDetails").find("uid").text = checklist_uuid

            parsed_checklist.find("checklistDetails").find("name").text = checklistname

            parsed_checklist.find("checklistDetails").find("description").text = checklist_description

            parsed_checklist.find("checklistDetails").find("startTime").text = start_time

        else:
            parsed_checklist = etree.fromstring(checklist_content)

            checklist_uuid = checklist_content.find("checklistDetails").find("uid").text

        for checklist_task in parsed_checklist.find("checklistTasks").findall("checklistTask"):
            parsed_checklist.find("checklistTasks").remove(checklist_task)
            parsed_checklist.find("checklistTasks").append(etree.fromstring(self.wintak_adapter.standardize_task(etree.tostring(checklist_task))))
        
        number = 0
        for checklist_task in parsed_checklist.find("checklistTasks").findall("checklistTask"):
            num = Element("number")
            checklist_task.append(num)
            num.text = str(number)
            number += 1

        try:
            self.persistency_controller.create_checklist(checklist_uuid)
        except Exception:
            pass

        checklist_task_list = self._save_tasks_in_checklist(parsed_checklist)

        self.request.set_value("synctype", "ExCheckChecklist")
        self.request.set_value("objectdata", etree.tostring(parsed_checklist, xml_declaration=True, encoding='UTF-8'))
        self.request.set_value("objectuid", checklist_uuid)
        self.request.set_value("objkeywords", ["Template"])
        self.request.set_value("objstarttime", start_time)
        self.request.set_value("tool", "ExCheck")
        self.request.set_value("mime_type", "application/xml")

        self.execute_sub_action("SaveEnterpriseSyncData")

        checklist_tasks = parsed_checklist.find("checklistTasks")

        # for checklist_task in checklist_task_list:
        #     checklist_tasks.append(checklist_task)
        checklist_string = etree.tostring(parsed_checklist, xml_declaration=True, encoding='UTF-8')

        self.request.set_value("mission_id", checklist_uuid)
        self.request.set_value("mission_data", b'')
        self.request.set_value("mission_data_args", {
            'defaultRole': "Owner",
            'downloaded': False,
            'connected': True,
            'isSubscribed': True,
            'autoPublish': False,
            'description': checklist_description,
            'uids': [],
            'contents': [
                {

                }
            ],
            'createTime': start_time,
            'passwordProtected': False,
            'groups': [],
            'serviceUri': '',
            'classification': 'UNCLASSIFIED'})
        self.request.set_value("creatorUid", "ExCheck")

        self.execute_sub_action("PutMission")

        self.response.set_value("checklist", checklist_string)
        return checklist_string
    
    def get_time(self):
        timer = dt
        now = timer.utcnow()
        return now.strftime(DATETIME_FMT)

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
        
        checklisttaskdata = self.wintak_adapter.standardize_task(checklisttaskdata)

        self.request.set_value("synctype", "ExCheckChecklistTask")
        self.request.set_value("objectdata", checklisttaskdata)
        self.request.set_value("objectuid", checklisttaskuid)
        self.request.set_value("objecthash", str(hashlib.sha256(checklisttaskdata).hexdigest()))
        self.execute_sub_action("UpdateEnterpriseSyncData")

        self.request.set_value("objectuid", checklistuid)
        sub_response = self.execute_sub_action("GetEnterpriseSyncData")
        checklist_data = sub_response.get_value("objectdata")

        checklist_data_elem = ElementTree.fromstring(checklist_data)
        checklist_tasks = checklist_data_elem.find("checklistTasks")

        tasks = checklist_tasks.findall("checklistTask")

        for task in tasks:
            if task.find("uid").text == checklisttaskuid:
                checklist_tasks.remove(task)
                checklist_tasks.append(ElementTree.fromstring(checklisttaskdata))
                break

        self.request.set_value("synctype", "ExCheckChecklist")
        self.request.set_value("objectdata", ElementTree.tostring(checklist_data_elem))
        self.request.set_value("objectuid", checklistuid)
        self.execute_sub_action("UpdateEnterpriseSyncData")

        return "done"
    
    def get_checklist(self, checklistuid: str, config_loader, *args, **kwargs) -> str:
        """get the contents of a checklist based on its UID

        Args:
            checklistuid (str): the uid of the checklist to be returned

        Returns:
            str: the content of the checklist
        """

        self.request.set_value("objectuid", checklistuid)

        sub_response = self.execute_sub_action("GetEnterpriseSyncData")

        checklist_content = ElementTree.fromstring(sub_response.get_value("objectdata"))

        # task_uids = []
        # for task in checklist_db.tasks:
        #     task_uids.append(task.PrimaryKey)
        
        # self.request.set_value("objectuids", task_uids)

        # sub_response = self.execute_sub_action("GetMultipleEnterpriseSyncData")

        # task_files = sub_response.get_value("objectdata")

        # checklist_with_tasks = self._add_tasks_to_checklist(checklist_content, task_files)
        # for task in checklist_content.find("checklistTasks"):
        #     check_uid = task.find("checklistUid")
        #     if check_uid is not None:
        #         task.remove(check_uid)
        
        checklist_string = ElementTree.tostring(checklist_content)

        self.response.set_value("checklist_data", checklist_string)

        return checklist_string
    
    def get_checklist_task(self, checklistuid, checklisttaskuid, *args, **kwargs):
        """get the contents of a checklist task on its UID

        Args:
            checklistuid (str): the uid of the checklist to be returned

        Returns:
            str: the content of the checklist
        """

        self.request.set_value("objectuid", checklisttaskuid)

        sub_response = self.execute_sub_action("GetEnterpriseSyncData")

        checklist_task_content = sub_response.get_value("objectdata")
        
        self.response.set_value("checklist_task_data", checklist_task_content)

        return checklist_task_content

    def get_all_checklists(self, config_loader, logger, *args, **kwargs):

        checklists = self.persistency_controller.get_all_checklists()

        checklist_uids = [checklist.PrimaryKey for checklist in checklists]

        self.request.set_value("objectuids", checklist_uids)

        self.request.set_value("use_bytes", True)

        sub_response = self.execute_sub_action("GetMultipleEnterpriseSyncData")

        checklist_contents = sub_response.get_value("objectdata")

        complete_checklists = Element("checklists")

        for checklist, checklist_content in zip(checklists, checklist_contents):
            try:
                checklist_obj = etree.fromstring(checklist_content)
                checklist_obj.remove(checklist_obj.find("checklistTasks"))
                checklist_obj.remove(checklist_obj.find("checklistColumns"))
                checklist_obj.append(Element("checklistColumns"))
                checklist_obj.append(Element("checklistTasks"))
                complete_checklists.append(checklist_obj)
            except Exception as ex:
                logger.error("error adding checklist to checklist content: %s", ex)
        checklists = etree.tostring(complete_checklists, encoding='UTF-8', method='xml', standalone="yes").replace(b"\n", b"")
        self.response.set_value("checklists", checklists)
        return checklists

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
            template_tasks.append(task_elem)

        return template_elem
    
    def create_checklist_task(self, checklistuid, taskuid, taskdata: Element, *args, **kwargs):
        """create a new template task in the db and the file system"""
        
        # in atak template tasks have no uid so one must be created artificially
        if taskuid is None:
            taskuid = str(uuid.uuid4())
        
        checklistuid_obj = taskdata.find("checklistUid")
        if checklistuid_obj is not None:
            checklistuid_obj.text = checklistuid

        taskdata.find("uid").text = taskuid
        
        self.request.set_value("synctype", "ExCheckChecklistTask")
        self.request.set_value("objectdata", ElementTree.tostring(taskdata))
        self.request.set_value("objectuid", taskuid)
        self.request.set_value("objkeywords", ["Task"])
        self.request.set_value("objstarttime", self.get_time())
        self.request.set_value("tool", "ExCheck")
        self.request.set_value("mime_type", "application/xml")

        self.execute_sub_action("SaveEnterpriseSyncData")

        self.persistency_controller.create_checklist_task(checklistuid, taskuid)

    def get_checklist_mission(self, checklist_id, config_loader, *args, **kwargss):
        mission_info = self.domain_controller.get_mission_info_object(config_loader)
        checklist_db_obj = self.persistency_controller.get_checklist(checklist_id)
        
        mission_uids = [checklist_task.PrimaryKey for checklist_task in checklist_db_obj.tasks]
        self.request.set_value("objectuids", mission_uids)
        sub_resp = self.execute_sub_action("GetMultipleEnterpriseSyncMetaData")

        mission_elements_metadata = sub_resp.get_value("objectmetadata")

        self.mission_controller.complete_mission_info(mission_info, mission_elements_metadata, checklist_id, config_loader)

        final_message = self.mission_controller.serialize_to_json(mission_info)
        
        self.response.set_value("mission_info", final_message[0])
        
        return final_message[0]
