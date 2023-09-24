from FreeTAKServer.components.core.domain.domain import Event

from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_COT_CONTENT
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.domain import details, location
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from FreeTAKServer.components.core.domain.domain import MissionContent
from FreeTAKServer.core.util.time_utils import get_dtg

class MissionCoTContentBuilder(Builder):
    """Builds a mission cot change object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: MissionContent = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a mission change object"""
        self.request.set_value("object_class_name", "MissionContent")

        configuration = config_loader.find_configuration(MISSION_COT_CONTENT)

        self.result = super()._create_model_object(configuration, extended_domain={"details": details, "location": location})
    
    def add_object_data(self, mapped_object: MissionCoT):
        """adds the data from the mapped object to the result object"""
        self.request.set_value("cot_id", mapped_object.uid)
        cot: 'Event' = self.execute_sub_action("GetCoT").get_value("cot")
        # set hardcoded values
        self.result.creatorUid = ""

        # set values from mapped object at root
        self.result.data = mapped_object.uid
        self.result.timestamp = cot.time
        
        # set values from mapped object at detail
        self.result.details.callsign = cot.detail.contact.callsign
        self.result.details.iconsetPath = cot.detail.usericon.iconsetpath
        self.result.details.type = cot.type

        self.result.details.location.lat = cot.point.lat
        self.result.details.location.lon = cot.point.lon

    def get_result(self):
        return self.result