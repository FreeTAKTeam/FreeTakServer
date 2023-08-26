from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty


class contact(CoTNode):
    def __init__(self, configuration, model):
        super().__init__(self.__class__.__name__, configuration, model)
        self.cot_attributes["callsign"] = None
        self.cot_attributes["endpoint"] = None
        self.cot_attributes["iconsetpath"] = None
        self.cot_attributes["uid"] = None
        self.cot_attributes["name"] = None
        self.cot_attributes["emailAddress"] = None
        self.cot_attributes["xmppUsername"] = None
        self.cot_attributes["sipAddress"] = None

    @CoTProperty
    def iconsetpath(self):
        return self.cot_attributes.get("iconsetpath", None)

    @iconsetpath.setter
    def iconsetpath(self, iconsetpath=None):
        self.cot_attributes["iconsetpath"] = iconsetpath

    @CoTProperty
    def sipAddress(self):
        return self.cot_attributes.get("sipAddress", None)

    @sipAddress.setter
    def sipAddress(self, sipAddress=None):
        self.cot_attributes["sipAddress"] = sipAddress

    @CoTProperty
    def emailAddress(self):
        return self.cot_attributes.get("emailAddress", None)

    @emailAddress.setter
    def emailAddress(self, emailAddress=None):
        self.cot_attributes["emailAddress"] = emailAddress

    @CoTProperty
    def xmppUsername(self):
        return self.cot_attributes.get("xmppUsername", None)

    @xmppUsername.setter
    def xmppUsername(self, xmppUsername=None):
        self.cot_attributes["xmppUsername"] = xmppUsername

    @CoTProperty
    def callsign(self):
        return self.cot_attributes.get("callsign", None)

    @callsign.setter
    def callsign(self, callsign=None):
        self.cot_attributes["callsign"] = callsign

    @CoTProperty
    def endpoint(self):
        return self.cot_attributes.get("endpoint", None)

    @endpoint.setter
    def endpoint(self, endpoint=None):
        self.cot_attributes["endpoint"] = endpoint

    @CoTProperty
    def uid(self):
        return self.cot_attributes.get("uid", None)

        # uid setter

    @uid.setter
    def uid(self, uid=None):
        self.uid = uid

    @CoTProperty
    def name(self):
        return self.cot_attributes.get("name", None)

    @name.setter
    def name(self, name=None):
        self.name = name

    @CoTProperty
    def phone(self):
        return self.cot_attributes.get("phone", None)

    @phone.setter
    def phone(self, phone=None):
        self.cot_attributes["phone"] = phone
