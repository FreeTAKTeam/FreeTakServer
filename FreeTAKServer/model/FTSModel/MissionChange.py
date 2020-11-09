from FreeTAKServer.model.FTSModel.ContentResource import ContentResource
from FreeTAKServer.model.FTSModel.CreatorUid import CreatorUid
from FreeTAKServer.model.FTSModel.MissionName import MissionName
from FreeTAKServer.model.FTSModel.Timestamp import Timestamp
from FreeTAKServer.model.FTSModel.Type import Type

class MissionChange:
    def __init__(self):
        pass
    @staticmethod
    def CreateExCheckTemplate():
        missionchange = MissionChange()
        missionchange.contentresource = ContentResource.CreateExCheckTemplate()
        missionchange.creatoruid = CreatorUid.CreateExCheckTemplate()
        missionchange.missionname = MissionName.CreateExCheckTemplate()
        missionchange.timestamp = Timestamp.CreateExCheckTemplate()
        missionchange.type = Type.CreateExCheckTemplate()
        return missionchange

