from digitalpy.model.load_configuration import Configuration
import uuid
from datetime import datetime as dt
from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty


class Event(CoTNode):
    def __init__(self, configuration: Configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
        self.cot_attributes["version"] = None
        self.cot_attributes["uid"] = None
        self.cot_attributes["type"] = None
        self.cot_attributes["how"] = None
        self.cot_attributes["stale"] = None
        self.cot_attributes["start"] = None
        self.cot_attributes["time"] = None

    @CoTProperty
    def start(self):
        return self.cot_attributes.get("start", None)

    @start.setter
    def start(self, start=0):
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        if start == None:
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            self.cot_attributes["start"] = zulu
        else:
            self.cot_attributes["start"] = start

    @CoTProperty
    def how(self):
        return self.cot_attributes.get("how", None)

    @how.setter
    def how(self, how=0):
        self.cot_attributes["how"] = how 

    @CoTProperty
    def uid(self):
        return self.cot_attributes.get("uid", None)

    @uid.setter
    def uid(self, uid):
        if uid is None:
            self.cot_attributes["uid"] = str(uuid.uuid1())

        else:
            self.cot_attributes["uid"] = uid

    @CoTProperty
    def version(self):
        return self.cot_attributes.get("version", None)

    @version.setter
    def version(self, version):
        self.cot_attributes["version"] = version

    @CoTProperty
    def time(self):
        return self.cot_attributes.get("time", None)

    @time.setter
    def time(self, time=0):
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        if time is None:
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            self.time = zulu
        else:
            self.cot_attributes["time"] = time

    @CoTProperty
    def stale(self):
        return self.cot_attributes.get("stale", None)

    @stale.setter
    def stale(self, stale=None, staletime=60):
        if stale is None:
            DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            add = dt.timedelta(seconds=staletime)
            stale_part = dt.datetime.strptime(zulu, DATETIME_FMT) + add
            self.cot_attributes["stale"] = stale_part.strftime(DATETIME_FMT)
        else:
            self.cot_attributes["stale"] = stale

    @CoTProperty
    def type(self):
        return self.cot_attributes.get("type", None)

    @type.setter
    def type(self, type=0):
        self.cot_attributes["type"] = type

    @CoTProperty
    def point(self):
        return self.cot_attributes.get("point", None)

    @point.setter
    def point(self, point=None):
        self.cot_attributes["point"] = point

    @CoTProperty
    def detail(self):
        return self.cot_attributes.get("detail", None)

    @detail.setter
    def detail(self, detail=None):
        self.cot_attributes["detail"] = detail

