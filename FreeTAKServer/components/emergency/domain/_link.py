from digitalpy.model.node import Node
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject

class link(Node, FTSProtocolObject):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
        self.uid = None
        self.relation = None
        self.production_time = None
        self.type = None
        self.parent_callsign = None

    def getremarks(self):
        return self.remarks

    def setremarks(self, remarks):
        self.__modified = True
        self.remarks = remarks

    def getcallsign(self):
        return self.callsign

    def setcallsign(self, callsign):
        self.__modified = True
        self.callsign = callsign

    def getpoint(self):
        return self.point

    def setpoint(self, point):
        self.__modified = True
        self.point = point

    # uid getter 
    def getuid(self):
        import uuid
        if self.uid:
            return self.uid
        else:
            self.uid = uuid.uuid1()
            return self.uid

    # uid setter 
    def setuid(self, uid=0):
        self.__modified = True
        self.uid=uid 

    # production_time getter 
    def getproduction_time(self): 
        return self.production_time 

    # production_time setter 
    def setproduction_time(self, production_time=0):
        self.__modified = True
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%SZ"
        if production_time == None:
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            add = dt.timedelta(minutes=1)
            production_time_part = dt.datetime.strptime(zulu, DATETIME_FMT) + add
            self.production_time = production_time_part.strftime(DATETIME_FMT)
        else:
            self.production_time = production_time

    # relation getter 
    def getrelation(self): 
        return self.relation 

    # relation setter 
    def setrelation(self, relation=0):
        self.__modified = True
        self.relation=relation 

    # type getter 
    def gettype(self): 
        return self.type 

    # type setter 
    def settype(self, type=0):
        self.__modified = True
        self.type=type 

    # parent_callsign getter 
    def getparent_callsign(self): 
        return self.parent_callsign 

    # parent_callsign setter 
    def setparent_callsign(self, parent_callsign=0):
        self.__modified = True
        self.parent_callsign=parent_callsign 

    def setrelationship(self, relationship):
        self.relationship=relationship

    def getrelationship(self):
        return self.relationship