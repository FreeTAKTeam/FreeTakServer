from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject


class ChecklistColumns(FTSProtocolObject):
    @staticmethod
    def Checklist():
        checklistcolumns = ChecklistColumns()
        return checklistcolumns
