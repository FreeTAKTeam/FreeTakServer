from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class checklistTasks(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)

    @CoTProperty
    def lineBreak(self):
        return self.__lineBreak

    @lineBreak.setter
    def lineBreak(self, lineBreak=None):
        self.__lineBreak = lineBreak

    @CoTProperty
    def number(self):
        return self.__number

    @number.setter
    def number(self, number=None):
        self.__number = number
    
    @CoTProperty
    def uid(self):
        return self.__uid

    @uid.setter
    def uid(self, uid=None):
        self.__uid = uid

    @CoTProperty
    def value(self):
        return self.__value

    @value.setter
    def value(self, value=None):
        self.__value = value

    @CoTProperty
    def status(self):
        return self.__status

    @status.setter
    def status(self, status=None):
        self.__status = status

    @CoTProperty
    def CompleteDTG(self):
        return self.__CompleteDTG

    @CompleteDTG.setter
    def CompleteDTG(self, CompleteDTG=None):
        self.__CompleteDTG = CompleteDTG
