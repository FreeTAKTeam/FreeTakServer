from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from datetime import datetime as dt
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty


class remarks(CoTNode):
    def __init__(self, configuration, model, registry=None):
        attributes = {}
        self.__keywords = None
        self.__relation = None
        self.__time = None
        self.__to = None
        self.__version = None
        super().__init__(self.__class__.__name__, configuration, model, registry, attributes)

    @CoTProperty
    def keywords(self):
        return self.__keywords

    @keywords.setter
    def keywords(self, keywords: str):
        self.__modified = True
        self.keywords = keywords

    @CoTProperty
    def source(self):
        return self.__source

    @source.setter
    def source(self, source: str):
        self.__modified = True
        self.source = source

    @CoTProperty
    def sourceID(self):
        return self.__sourceID

    @sourceID.setter
    def sourceID(self, sourceID: str):
        self.__modified = True
        self.sourceID = sourceID

    @CoTProperty
    def time(self):
        return self.__time

    @time.setter
    def time(self, time: dt):
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
        return self.__to

    @to.setter
    def to(self, to: str):
        self.__to = to

    @CoTProperty
    def version(self):
        return self.__version

    @version.setter
    def version(self, version: str):
        self.__version = version

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text
