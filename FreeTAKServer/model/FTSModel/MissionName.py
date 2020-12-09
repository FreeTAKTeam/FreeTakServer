from FreeTAKServer.model.FTSModelVariables.MissionNameVariables import MissionNameVariables as vars

class MissionName:
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def CreateExCheckTemplate(INTAG=vars.CreateExCheckTemplate().INTAG, ):
        missionname = MissionName()

        missionname.setINTAG(INTAG)

        return missionname

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG

