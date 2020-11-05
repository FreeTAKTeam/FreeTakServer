from FreeTAKServer.model.FTSModel.MissionChange import MissionChange

class MissionChanges:
    def __init__(self):
        pass

    @staticmethod
    def CreateExCheckTemplate():
        missionchanges = MissionChanges()
        missionchanges.missionchange = MissionChange.CreateExCheckTemplate()
        return missionchanges

