from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from datetime import datetime as dt
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty


class remarks(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
        self.cot_attributes["keywords"] = None
        self.cot_attributes["relation"] = None
        self.cot_attributes["time"] = None
        self.cot_attributes["to"] = None
        self.cot_attributes["version"] = None

    @CoTProperty
    def keywords(self):
        return self.cot_attributes.get("keywords", None)

    @keywords.setter
    def keywords(self, keywords):
        self.__modified = True
        self.keywords = keywords

    @CoTProperty
    def source(self):
        return self.cot_attributes.get("source", None)

    @source.setter
    def source(self, source):
        self.__modified = True
        self.source = source

    @CoTProperty
    def sourceID(self):
        return self.cot_attributes.get("sourceID", None)

    @sourceID.setter
    def sourceID(self, sourceID):
        self.__modified = True
        self.sourceID = sourceID

    @CoTProperty
    def time(self):
        return self.cot_attributes.get("time", None)

    @time.setter
    def time(self, time=0):
        self.__modified = True
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%SZ"
        if time == None:
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            add = dt.timedelta(minutes=1)
            production_time_part = dt.datetime.strptime(zulu, DATETIME_FMT) + add
            self.time = production_time_part.strftime(DATETIME_FMT)
        else:
            self.time = time

    @CoTProperty
    def to(self):
        return self.cot_attributes.get("to", None)

    @to.setter
    def to(self, to):
        self.cot_attributes["to"] = to

    @CoTProperty
    def version(self):
        return self.cot_attributes.get("version", None)

    @version.setter
    def version(self, version=0):
        self.cot_attributes["version"] = version

    @property
    def text(self):
        return self.cot_attributes.get("text", None)

    @text.setter
    def text(self, text):
        self.cot_attributes["text"] = text
