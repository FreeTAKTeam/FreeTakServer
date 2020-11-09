from FreeTAKServer.model.FTSModelVariables.SubmissionTimeVariables import SubmissionTimeVariables as vars

class SubmissionTime:
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def CreateExCheckTemplate(INTAG=vars.CreateExCheckTemplate().INTAG, ):
        submissiontime = SubmissionTime()

        submissiontime.setINTAG(INTAG)

        return submissiontime

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG