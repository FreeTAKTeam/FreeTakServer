from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_RECORD
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.domain import detail
from FreeTAKServer.components.extended.mission.persistence.mission import Mission as DBMission
from FreeTAKServer.components.core.domain.domain import MissionData
from FreeTAKServer.core.util.time_utils import get_dtg

class MissionListRecordBuilder(Builder):
    """Builds a mission cot change object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: MissionData = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a mission change object"""
        self.request.set_value("object_class_name", "MissionData")

        configuration = config_loader.find_configuration(MISSION_RECORD)

        self.result = super()._create_model_object(configuration)

    def add_object_data(self, mapped_object: DBMission):
        """adds the data from the mapped object to the mission """
        if mapped_object == None:
            return
        self.result.name = mapped_object.name
        self.result.description = mapped_object.description
        self.result.chatRoom = mapped_object.chatRoom
        self.result.baseLayer = mapped_object.baseLayer
        self.result.bbox = mapped_object.bbox
        self.result.path = mapped_object.path
        self.result.classification = mapped_object.classification
        self.result.tool = "public"
        self.result.keywords = []
        self.result.creatorUid = mapped_object.creatorUid
        # TODO: get time dynamically
        self.result.createTime = get_dtg(mapped_object.createTime)
        
        # self.result.groups = mapped_object.groups
        
        self.result.groups = []
        
        # self.result.externalData = mapped_object.externalData
        # self.result.feeds = mapped_object.feeds

        self.result.feeds = []
        
        # self.result.mapLayers = mapped_object.mapLayers
        
        self.result.mapLayers = []
        self.result.inviteOnly = False if mapped_object.inviteOnly == 0 else True
        self.result.expiration = mapped_object.expiration
        
        # self.result.uids = mapped_object.uids
        
        self.result.passwordProtected = False if mapped_object.passwordProtected == "False" else True
        
    def get_result(self):
        """gets the result of the builder"""
        return self.result