from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModel.MissionChange import MissionChange


class MissionChanges(FTSProtocolObject):
    def __init__(self):
        pass

    @staticmethod
    def ExcheckUpdate():
        missionchanges = MissionChanges()
        missionchanges.MissionChange = MissionChange.ExcheckUpdate()
        return missionchanges
