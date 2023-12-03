from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.parsing.load_configuration import LoadConfiguration

from lxml import etree

from FreeTAKServer.components.core.domain.domain import Event

from ..persistence.detail import Detail as DBDetail
from ..persistence.event import Event as DBEvent
from ..persistence.point import Point as DBPoint

from ..configuration.cot_management_constants import (
    BASE_OBJECT,
)

class CoTManagementDomainController(Controller):
    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        
    def initialize(self, request, response):
        super().initialize(request, response)
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def create_standard_xml(self, config_loader, *args, **kwargs) -> Event:
        self.request.set_value("object_class_name", "Event")
        
        configuration = config_loader.find_configuration(BASE_OBJECT)

        return self.create_model_object(configuration, extended_domain = {})


    def complete_standard_xml(self, event: Event, db_event: DBEvent):
        """
        This method completes the standard XML for an event object.
        """
        event.how = db_event.how
        event.time = db_event.time
        event.start = db_event.start
        event.stale = db_event.stale
        event.type = db_event.type
        event.uid = db_event.uid
        event.version = '2.0'

        point = event.point
        point.ce = db_event.point.ce
        point.hae = db_event.point.hae
        point.le = db_event.point.le
        point.lat = db_event.point.lat
        point.lon = db_event.point.lon

        detail = event.detail
        detail.usericon.iconsetpath = db_event.detail.usericon.iconsetpath
        detail.contact.callsign = db_event.detail.contact.callsign
        self.request.set_value("xml", db_event.detail.xml_content)
        self.request.set_value("object_class_name", "Detail")
        self.request.set_value("model_object", detail)
        detail_completed = self.execute_sub_action("XMLToNode").get_value("model_object")
        
        event.detail = detail_completed
        return event

    def create_model_object(self, configuration, extended_domain={}, *args, **kwargs):
        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", extended_domain)

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        model_object = response.get_value("model_object")
        
        return model_object