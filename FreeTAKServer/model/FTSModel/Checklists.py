from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModel.Checklist import Checklist

class Checklists(FTSProtocolObject):
    def __init__(self):
        self.checklist = []
        self.__index = 0
    @staticmethod
    def Checklist():
        checklists = Checklists()
        checklists.checklist = []
        return checklists

    def setchecklist(self, checklistitem):
        self.checklist.append(checklistitem)

    def getchecklist(self):
        item = self.__index
        self.__index += 1
        return self.checklist[item]
