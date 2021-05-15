from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.Link_attrVariables import Link_attrVariables as vars

class Link_attr(FTSProtocolObject):
    def __init__(self):
        self.color = None
        self.type = None
        self.method = None
        self.direction = None
        self.routetype = None
        self.order = None

    @staticmethod
    def Route(COLOR = vars.Route().COLOR, TYPE = vars.Route().TYPE, METHOD = vars.Route().METHOD, DIRECTION = vars.Route().DIRECTION, ROUTETYPE = vars.Route().ROUTETYPE, ORDER = vars.Route().ORDER):
        link_attr = Link_attr()
        link_attr.setcolor(COLOR)
        link_attr.settype(TYPE)
        link_attr.setorder(ORDER)
        link_attr.setmethod(METHOD)
        link_attr.setdirection(DIRECTION)
        link_attr.setroutetype(ROUTETYPE)
        return link_attr

    def setcolor(self, color):
        self.color = color

    def getcolor(self):
        return self.color

    def settype(self, type):
        self.type = type

    def gettype(self):
        return self.type

    def getmethod(self):
        return self.method

    def setmethod(self, method):
        self.method = method
    def setdirection(self, direction):
        self.direction = direction
    def getdirection(self):
        return self.direction
    def getroutetype(self):
        return self.routetype
    def setroutetype(self, routetype):
        self.routetype = routetype
    def setorder(self, order):
        self.order = order
    def getorder(self):
        return self.order