from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModel.ChecklistColumns import ChecklistColumns
from FreeTAKServer.model.FTSModel.ChecklistDetails import ChecklistDetails
from FreeTAKServer.model.FTSModel.ChecklistTasks import ChecklistTasks

class Checklist(FTSProtocolObject):
    @staticmethod
    def Checklist():
        checklist = Checklist()
        checklist.checklistDetails = ChecklistDetails.Checklist()
        checklist.checklistColumns = ChecklistColumns.Checklist()
        checklist.checklistTasks = ChecklistTasks.Checklist()
        return checklist