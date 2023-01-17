from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.components.core.abstract_component.cot_property import CoTProperty


class contact(CoTNode):
    def __init__(self, configuration, model, registry=None):
        attributes = {}
        self.__callsign = None
        self.__endpoint = None
        self.__iconsetpath = None
        self.__uid = None
        self.__name = None
        self.__emailAddress = None
        self.__xmppUsername = None
        self.__sipAddress = None
        super().__init__(self.__class__.__name__, configuration, model, registry, attributes)

    @CoTProperty
    def iconsetpath(self):
        return self.__iconsetpath

    @iconsetpath.setter
    def iconsetpath(self, iconsetpath=None):
        self.__iconsetpath = iconsetpath

    @CoTProperty
    def sipAddress(self):
        return self.__sipAddress

    @sipAddress.setter
    def sipAddress(self, sipAddress=None):
        self.__sipAddress = sipAddress

    @CoTProperty
    def emailAddress(self):
        return self.__emailAddress

    @emailAddress.setter
    def emailAddress(self, emailAddress=None):
        self.__emailAddress = emailAddress

    @CoTProperty
    def xmppUsername(self):
        return self.__xmppUsername

    @xmppUsername.setter
    def xmppUsername(self, xmppUsername=None):
        self.__xmppUsername = xmppUsername

    @CoTProperty
    def callsign(self):
        return self.__callsign

    @callsign.setter
    def callsign(self, callsign=None):
        self.__callsign = callsign

    @CoTProperty
    def endpoint(self):
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, endpoint=None):
        self.__endpoint = endpoint

    @CoTProperty
    def uid(self):
        return self.__uid

        # uid setter

    @uid.setter
    def uid(self, uid=None):
        self.uid = uid

    @CoTProperty
    def name(self):
        return self.__name

    @name.setter
    def name(self, name=None):
        self.name = name

    @CoTProperty
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone=None):
        self.phone = phone
