from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
import datetime as dt

class timestamp(CoTNode):
    DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

    def __init__(self, configuration, model, oid=None):
        super().__init__(self.__class__.__name__, configuration, model, oid)
        self.cot_attributes["text"] = None

    @property
    def text(self):
        return self.cot_attributes.get("text", None)

    @text.setter
    def text(self, value):
        if value is None:
            now = dt.datetime.utcnow()
            zulu = now.strftime(self.DATETIME_FMT)
            self.cot_attributes["text"] = zulu
        else:
            self.cot_attributes["text"] = value
