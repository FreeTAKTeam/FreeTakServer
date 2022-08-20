from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from datetime import datetime as dt
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty

class link(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
        self.cot_attributes["uid"] = None
        self.cot_attributes["relation"] = None
        self.cot_attributes["production_time"] = None
        self.cot_attributes["type"] = None
        self.cot_attributes["parent_callsign"] = None

    @CoTProperty
    def remarks(self):
        return self.cot_attributes.get("remarks", None)

    @remarks.setter
    def remarks(self, remarks):
        self.__modified = True
        self.remarks = remarks

    @CoTProperty
    def callsign(self):
        return self.cot_attributes.get("callsign", None)

    @callsign.setter
    def callsign(self, callsign):
        self.__modified = True
        self.callsign = callsign

    @CoTProperty
    def point(self):
        return self.cot_attributes.get("point", None)

    @point.setter
    def point(self, point):
        self.__modified = True
        self.point = point

    @CoTProperty 
    def uid(self):
        import uuid
        if "uid" in self.cot_attributes:
            return self.cot_attributes.get("uid", None)
        else:
            self.cot_attributes["uid"] = uuid.uuid1()
            return self.cot_attributes.get("uid", None)

    @uid.setter 
    def uid(self, uid=0):
        self.__modified = True
        self.cot_attributes["uid"]=uid 

    @CoTProperty 
    def production_time(self): 
        return self.cot_attributes.get("production_time", None)

    @production_time.setter
    def production_time(self, production_time=0):
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

    @CoTProperty
    def relation(self): 
        return self.cot_attributes.get("relation", None)

    @relation.setter
    def relation(self, relation=0):
        self.__modified = True
        self.cot_attributes["relation"]=relation 

    @CoTProperty 
    def type(self): 
        return self.cot_attributes.get("type", None)

    @type.setter 
    def type(self, type=0):
        self.__modified = True
        self.cot_attributes["type"]=type 

    @CoTProperty 
    def parent_callsign(self): 
        return self.cot_attributes.get("parent_callsign", None)

    @parent_callsign.setter 
    def parent_callsign(self, parent_callsign=0):
        self.__modified = True
        self.cot_attributes["parent_callsign"]=parent_callsign 

    @CoTProperty
    def relationship(self):
        return self.cot_attributes.get("relationship", None)

    @relationship.setter
    def relationship(self, relationship):
        self.cot_attributes["relationship"]=relationship

