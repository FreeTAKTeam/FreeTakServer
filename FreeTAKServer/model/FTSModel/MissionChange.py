from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModel.ContentResource import ContentResource
from FreeTAKServer.model.FTSModel.CreatorUid import CreatorUid
from FreeTAKServer.model.FTSModel.MissionName import MissionName
from FreeTAKServer.model.FTSModel.Timestamp import Timestamp
from FreeTAKServer.model.FTSModel.Type import Type


class MissionChange(FTSProtocolObject):
    def __init__(self):
        pass

    @staticmethod
    def ExcheckUpdate():
        missionchange = MissionChange()
        missionchange.contentResource = ContentResource.ExcheckUpdate()
        missionchange.creatorUid = CreatorUid.ExcheckUpdate()
        missionchange.missionName = MissionName.ExcheckUpdate()
        missionchange.timestamp = Timestamp.ExcheckUpdate()
        missionchange.type = Type.ExcheckUpdate()
        return missionchange
