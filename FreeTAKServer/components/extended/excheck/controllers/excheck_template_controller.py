from typing import List
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from defusedxml import ElementTree

from lxml.etree import Element

from .excheck_persistency_controller import ExCheckPersistencyController

from ..configuration.excheck_constants import (
    BASE_OBJECT,
    BASE_OBJECT_NAME,
)

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
        
        self.persistency_controller.create_template(template_uid)

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

    def get_template(self, templateuid: str, *args, **kwargs) -> str:
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

        sub_response = self.execute_sub_action("GetManyEnterpriseSyncData")

        task_files = sub_response.get_value("objectdata")

        template_with_tasks = self._add_tasks_to_template(template_content, task_files)

        return ElementTree.tostring(template_with_tasks)
    
    def get_all_templates(self, *args, **kwargs):
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

            sub_response = self.execute_sub_action("GetManyEnterpriseSyncData")

            task_files = sub_response.get_value("objectdata")

            template_with_tasks = self._add_tasks_to_template(template_content, task_files)

            complete_templates.append(ElementTree.tostring(template_with_tasks))

        return complete_templates

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

        return template
    
    def create_template_task(self, templateuid, taskuid, taskdata, *args, **kwargs):
        """create a new template task in the db and the file system"""
        self.request.set_value("synctype", "ExCheckTemplateTask")
        self.request.set_value("objectdata", taskdata)
        self.request.set_value("objectuid", taskuid)

        self.execute_sub_action("SaveEnterpriseSyncData")

        self.persistency_controller.create_template_task(templateuid, taskuid)