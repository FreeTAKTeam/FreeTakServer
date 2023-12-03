from typing import List
import uuid
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from defusedxml import ElementTree

import hashlib

from xml.etree.ElementTree import Element

from FreeTAKServer.core.configuration.MainConfig import MainConfig

from .excheck_persistency_controller import ExCheckPersistencyController

from ..configuration.excheck_constants import (
    BASE_OBJECT,
    BASE_OBJECT_NAME,
    TEMPLATE_CONTENT,
    TEMPLATE_METADATA
)

config = MainConfig.instance()

class ExCheckWintakAdapter(Controller):
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

    def standardize_task(self, task: str):
        task_elem = ElementTree.fromstring(task)
        
        self.remove_Status(task_elem)
        
        #self.remove_duedtg(task_elem)

        self.remove_checklistuid(task_elem)
        
        #self.remove_completeDtg(task_elem)

        self.rename_completeDtg(task_elem)
        
        #self.remove_customstatus(task_elem)
        
        return ElementTree.tostring(task_elem)

    def remove_customstatus(self, task_elem):
        customStatus = task_elem.find("customStatus")
        if customStatus != None:
            task_elem.remove(customStatus)

    def remove_completeDtg(self, task_elem):
        completeDTG = task_elem.find("CompleteDTG")
        if completeDTG != None:
            task_elem.remove(completeDTG)
        alt_completeDTG = task_elem.find("completeDTG")
        if alt_completeDTG != None:
            task_elem.rremove(alt_completeDTG)

    def rename_completeDtg(self, task_elem):
        completeDTG = task_elem.find("CompleteDTG")
        if completeDTG != None:
            task_elem.remove(completeDTG)
            correct_dtg = task_elem.find("completeDTG")
            if correct_dtg != None:
                correct_dtg.text = completeDTG.text
            else:
                correct_dtg = Element("completeDTG")
                correct_dtg.text = completeDTG.text
                task_elem.append(correct_dtg)

    def remove_checklistuid(self, task_elem):
        checklist_uid = task_elem.find("checklistUid")
        if checklist_uid != None:
            task_elem.remove(checklist_uid)

    def remove_duedtg(self, task_elem):
        due_relative_time = task_elem.find("dueRelativeTime")
        if due_relative_time != None:
            task_elem.remove(due_relative_time)

    def remove_Status(self, task_elem):
        prev_status = task_elem.find("Status")
        if prev_status != None:
            task_elem.remove(prev_status)
