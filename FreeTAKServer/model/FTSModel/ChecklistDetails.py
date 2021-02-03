from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModel.Name import Name
from FreeTAKServer.model.FTSModel.Uid import Uid
from FreeTAKServer.model.FTSModel.Description import Description
from FreeTAKServer.model.FTSModel.StartTime import StartTime
from FreeTAKServer.model.FTSModel.CreatorUid import CreatorUid
from FreeTAKServer.model.FTSModel.CreatorCallsign import CreatorCallsign


class ChecklistDetails(FTSProtocolObject):
    @staticmethod
    def Checklist():
        checklistdetails = ChecklistDetails()
        checklistdetails.name = Name.Checklist()
        checklistdetails.uid = Uid.Checklist()
        checklistdetails.description = Description.Checklist()
        checklistdetails.starttime = StartTime.Checklist()
        checklistdetails.creatoruid = CreatorUid.Checklist()
        checklistdetails.creatorcallsign = CreatorCallsign.Checklist()
        return checklistdetails
