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

DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

config = MainConfig.instance()

class ExCheckXMLController(Controller):
    """manage template operations"""
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

    def calculate_external_data_update_notes(self, updated_task: str, checklist: str, user: str, *args, **kwargs):
        """return the notes for an external data update notification in the form, USER completed CHECKLISTNAME; COLUMNNAME:: NEWVALUE

        Args:
            updated_task (ElementTree): the xml contents of the updated task
            checklist (ElementTree): the xml contents of the checklist
            user (str): the user who updated the task
        """

        checklist_name = checklist.find("checklistDetails").find("name").text

        return f"{user} completed {checklist_name}; {self.get_column_from_checklist_by_index(checklist, 0).find('columnName').text}: { updated_task.findall('value')[0].text}"

    def get_column_from_checklist_by_index(self, checklist: ElementTree, column_index: str, *args, **kwargs):
        """get a column from a checklist by index

        Args:
            checklists (ElementTree): the xml contents of a checklist
        """
        i = 0
        for column in checklist.findall("checklistColumns")[0].findall("checklistColumn"):
            if i == column_index:
                return column
            i+=1
        return None
    
    def get_column_index_from_checklist_by_name(self, checklist_data: str, column_name: str, *args, **kwargs):
        """get a column index from a checklist by name

        Args:
            checklist_data (str): the xml contents of a checklist
        """
        checklist = ElementTree.fromstring(checklist_data)
        
        i=-1
        for column in checklist.findall("column"):
            i+=1
            if column.attrib["name"] == column_name:
                return i
        return None

    def get_task_from_checklist_by_id(self, checklist_data: str, task_id: str, *args, **kwargs):
        """get a task from a checklist by id

        Args:
            checklist_data (str): the xml contents of a checklist
        """
        checklist = ElementTree.fromstring(checklist_data)
        for task in checklist.findall("task"):
            if task.attrib["uid"] == task_id:
                return task
        return None