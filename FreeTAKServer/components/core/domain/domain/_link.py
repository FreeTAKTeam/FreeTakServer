from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from datetime import datetime as dt
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty


class link(CoTNode):
    def __init__(self, configuration, model, registry=None):
        attributes = {}
        self.__uid = None
        self.__relation = None
        self.__production_time = None
        self.__type = None
        self.__parent_callsign = None
        super().__init__(self.__class__.__name__, configuration, model, registry, attributes)

    @CoTProperty
    def remarks(self):
        return self.__remarks

    @remarks.setter
    def remarks(self, remarks: str):
        self.__modified = True
        self.__remarks = remarks

    @CoTProperty
    def callsign(self):
        return self.__callsign

    @callsign.setter
    def callsign(self, callsign: str):
        self.__callsign = callsign

    @CoTProperty
    def point(self):
        return self.__point

    @point.setter
    def point(self, point):
        self.__point = point

    @CoTProperty
    def uid(self):
        import uuid

        if "uid" in self.cot_attributes:
            return self.__uid
        else:
            self.__uid = uuid.uuid1()
            return self.__uid

    @uid.setter
    def uid(self, uid: str):
        self.__modified = True
        self.__uid = uid

    @CoTProperty
    def production_time(self):
        return self.__production_time

    @production_time.setter
    def production_time(self, production_time: dt):
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
        return self.__relation

    @relation.setter
    def relation(self, relation: str):
        self.__modified = True
        self.__relation = relation

    @CoTProperty
    def type(self):
        return self.__type

    @type.setter
    def type(self, type: str):
        self.__modified = True
        self.__type = type

    @CoTProperty
    def parent_callsign(self):
        return self.__parent_callsign

    @parent_callsign.setter
    def parent_callsign(self, parent_callsign: str):
        self.__modified = True
        self.__parent_callsign = parent_callsign

    @CoTProperty
    def relationship(self):
        return self.__relationship

    @relationship.setter
    def relationship(self, relationship: str):
        self.__relationship = relationship
