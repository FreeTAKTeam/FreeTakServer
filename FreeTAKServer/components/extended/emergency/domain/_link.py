from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from datetime import datetime as dt

class link(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
        self.cot_attributes["uid"] = None
        self.cot_attributes["relation"] = None
        self.cot_attributes["production_time"] = None
        self.cot_attributes["type"] = None
        self.cot_attributes["parent_callsign"] = None

    def getremarks(self):
        return self.cot_attributes["remarks"]

    def setremarks(self, remarks):
        self.__modified = True
        self.remarks = remarks

    def getcallsign(self):
        return self.cot_attributes["callsign"]

    def setcallsign(self, callsign):
        self.__modified = True
        self.callsign = callsign

    def getpoint(self):
        return self.cot_attributes["point"]

    def setpoint(self, point):
        self.__modified = True
        self.point = point

    # uid getter 
    def getuid(self):
        import uuid
        if "uid" in self.cot_attributes:
            return self.cot_attributes["uid"]
        else:
            self.cot_attributes["uid"] = uuid.uuid1()
            return self.cot_attributes["uid"]

    # uid setter 
    def setuid(self, uid=0):
        self.__modified = True
        self.cot_attributes["uid"]=uid 

    # production_time getter 
    def getproduction_time(self): 
        return self.cot_attributes["production_time"]

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
        return self.cot_attributes["relation"]

    # relation setter 
    def setrelation(self, relation=0):
        self.__modified = True
        self.cot_attributes["relation"]=relation 

    # type getter 
    def gettype(self): 
        return self.cot_attributes["type"]

    # type setter 
    def settype(self, type=0):
        self.__modified = True
        self.cot_attributes["type"]=type 

    # parent_callsign getter 
    def getparent_callsign(self): 
        return self.cot_attributes["parent_callsign"]

    # parent_callsign setter 
    def setparent_callsign(self, parent_callsign=0):
        self.__modified = True
        self.cot_attributes["parent_callsign"]=parent_callsign 

    def setrelationship(self, relationship):
        self.cot_attributes["relationship"]=relationship

    def getrelationship(self):
        return self.cot_attributes["relationship"]