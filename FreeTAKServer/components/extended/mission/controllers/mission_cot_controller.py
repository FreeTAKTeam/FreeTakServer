import json
from typing import List, Dict, TYPE_CHECKING
from FreeTAKServer.components.extended.excheck.domain.mission_data import MissionData
from FreeTAKServer.components.extended.mission.controllers.mission_domain_controller import MissionDomainController
from FreeTAKServer.components.extended.mission.controllers.mission_logs_controller import (
    MissionLogsController,
)
from FreeTAKServer.components.extended.mission.controllers.mission_change_controller import (
    MissionChangeController,
)
from FreeTAKServer.components.extended.mission.controllers.mission_external_data_controller import (
    MissionExternalDataController,
)
from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import (
    MissionPersistenceController,
)
from FreeTAKServer.components.core.fts_domain.domain import mission
from FreeTAKServer.core.util.serialization_utils import serialize_to_json
from FreeTAKServer.core.util.time_utils import (
    get_datetime_from_dtg,
    get_current_datetime,
    get_current_dtg
)
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from FreeTAKServer.core.configuration.MainConfig import MainConfig

from lxml import etree

if TYPE_CHECKING:
    from FreeTAKServer.components.core.fts_domain.domain import event

config = MainConfig.instance()


class MissionCOTController(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.persistence_controller = MissionPersistenceController(
            request, response, sync_action_mapper, configuration
        )
        self.change_controller = MissionChangeController(
            request, response, sync_action_mapper, configuration
        )
        self.domain_controller = MissionDomainController(
            request, response, sync_action_mapper, configuration
        )
        self.log_controller = MissionLogsController(
            request, response, sync_action_mapper, configuration
        )

    def initialize(self, request, response):
        super().initialize(request, response)
        self.persistence_controller.initialize(request, response)
        self.change_controller.initialize(request, response)
        self.domain_controller.initialize(request, response)
        self.log_controller.initialize(request, response)

    def get_mission_cots(self, mission_id, config_loader, *args, **kwargs):
        """returns all cots for a mission"""
        
        mission_cots = self.persistence_controller.get_mission_cots(mission_id)

        events = self.domain_controller.create_events(config_loader)

        self.request.set_value("object_class_name", "event")
        
        for cot in mission_cots:
            self.request.set_value("cot_id", cot.uid)
            cot_obj: 'event' = self.execute_sub_action("GetCoT").get_value("cot")
            
            self.request.set_value("node", cot_obj)

            xml_content = self.execute_sub_action("NodeToXML").get_value("message")

            events.xml.append(etree.fromstring(xml_content))
        
        self.request.set_value("node", events)
        xml_events= self.execute_sub_action("NodeToXML").get_value("message")
        self.response.set_value("cots", xml_events)
        return xml_events

    def create_mission_cot(
        self,
        mission_ids,
        uid,
        config_loader,
        *args,
        **kwargs
    ):
        """saves a CoT to a mission"""

        
        for mission_id in mission_ids:
            self.persistence_controller.create_mission_cot(
                mission_id=mission_id,
                uid=uid,
            )
            self.change_controller.create_mission_cot_record(
                mission_cot_uid=mission_id, cot_uid=uid, creator_uid=""
            )
            self.response.set_value("mission_cot_id", uid)
            self.response.set_context("mission")
            self.response.set_action("MissionCotCreatedNotification")

    def create_mission_geofence(
        self,
        mission_ids,
        cot_type,
        callsign,
        uid,
        iconset_path,
        lat,
        lon,
        xml_content,
        config_loader,
        *args,
        **kwargs
    ):
        """saves a geofence to a mission"""
        self.create_mission_cot(mission_ids=mission_ids, cot_type=cot_type, callsign=callsign, uid=uid, iconset_path=iconset_path, lat=lat, lon=lon, xml_content=xml_content, config_loader=config_loader)

    def create_mission_video_alias(
        self,
        mission_ids,
        cot_type,
        callsign,
        uid,
        iconset_path,
        lat,
        lon,
        xml_content,
        config_loader,
        *args,
        **kwargs
    ):
        """saves a video alias to a mission"""
        self.create_mission_cot(mission_ids=mission_ids, cot_type=cot_type, callsign=callsign, uid=uid, iconset_path=iconset_path, lat=lat, lon=lon, xml_content=xml_content, config_loader=config_loader)
