from typing import TYPE_CHECKING

from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_EXTERNAL_DATA
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.persistence.external_data import ExternalData
from FreeTAKServer.components.core.fts_domain.domain import MissionExternalData
from FreeTAKServer.core.util.time_utils import get_dtg

if TYPE_CHECKING:
    from FreeTAKServer.components.core.fts_domain.domain import event


class MissionStandardExternalDataBuilder(Builder):
    """Builds a mission external data object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: MissionExternalData = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a mission change object"""
        self.request.set_value("object_class_name", "MissionExternalData")

        configuration = config_loader.find_configuration(MISSION_EXTERNAL_DATA)

        self.result = super()._create_model_object(configuration, extended_domain={"MissionExternalData": MissionExternalData})

    def add_object_data(self, mapped_object: ExternalData):
        """adds the data from the mapped object to the mission """
        self.result.name = mapped_object.name
        self.result.tool = mapped_object.tool
        self.result.notes = mapped_object.notes
        self.result.uid = mapped_object.uid
        self.result.urlData = mapped_object.urlData
        self.result.urlView = mapped_object.urlView
        
    def get_result(self):
        """gets the result of the builder"""
        return self.result