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
        
        prev_status = task_elem.find("Status")
        if prev_status != None:
            task_elem.remove(prev_status)
            updated_status = Element("status")
            updated_status.text = prev_status.text
            task_elem.append(updated_status)
        
        due_relative_time = task_elem.find("dueRelativeTime")
        if due_relative_time != None:
            task_elem.remove(due_relative_time)

        checklist_uid = task_elem.find("checklistUid")
        if checklist_uid != None:
            task_elem.remove(checklist_uid)
        
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
        
        customStatus = task_elem.find("customStatus")
        if customStatus != None:
            task_elem.remove(customStatus)
        
        return ElementTree.tostring(task_elem)
