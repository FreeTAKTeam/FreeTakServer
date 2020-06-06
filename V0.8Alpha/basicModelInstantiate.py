from lxml import etree
from model.Event import Event

class basicModelInstantiate:
    def __init__(self, root, modelObject):
        try:
            self.modelObject = modelObject
            root = root.encode()
            self.event = etree.XML(root)
            self.establishVariables()
            self.eventAtrib()
            self.pointAtrib()
            print(root)
            self.takvAtrib()
            self.contactAtrib()
            self.uidAtrib()
            self.precisionlocationAtrib()
            self.groupAtrib()
            self.statusAtrib()
            self.trackAtrib()
        except Exception as e:
            print(e)

    def establishVariables(self):
        self.detail = self.event.find('detail')
        self.point = self.event.find('point')
        self.takv = self.detail.find('takv')
        self.contact = self.detail.find('contact')
        self.uid = self.detail.find('uid')
        self.precisionlocation = self.detail.find('precisionlocation')
        self.group = self.detail.find('__group')
        self.status = self.detail.find('status')
        self.track = self.detail.find('track')

    def eventAtrib(self):
        self.modelObject.uid = self.event.attrib['uid']
        self.modelObject.type = self.event.attrib['type']
        self.modelObject.how = self.event.attrib['how']

    def pointAtrib(self):
        self.modelObject.m_point.lat = self.point.attrib['lat']
        self.modelObject.m_point.lat = self.point.attrib['lon']
        self.modelObject.m_point.lat = self.point.attrib['hae']
        self.modelObject.m_point.lat = self.point.attrib['ce']
        self.modelObject.m_point.lat = self.point.attrib['le']

    def takvAtrib(self):
        self.modelObject.m_detail.m_takv.os = self.takv.attrib['os']
        self.modelObject.m_detail.m_takv.device = self.takv.attrib['device']
        self.modelObject.m_detail.m_takv.platform = self.takv.attrib['platform']
        self.modelObject.m_detail.m_takv.version = self.takv.attrib['version']

    def contactAtrib(self):
        self.modelObject.m_detail.m_contact.endpoint = self.contact.attrib['endpoint']
        self.modelObject.m_detail.m_contact.callsign = self.contact.attrib['callsign']
    
    def uidAtrib(self):
        self.modelObject.m_detail.m_uid.Droid = self.uid.attrib['Droid']
    
    def precisionlocationAtrib(self):
        self.modelObject.m_detail.m_precisionlocation.altsrc = self.precisionlocation.attrib['altsrc']
        self.modelObject.m_detail.m_precisionlocation.geopointsrc = self.precisionlocation.attrib['geopointsrc']

    def groupAtrib(self):
        self.modelObject.m_detail.m_group.role = self.group.attrib['role']
        self.modelObject.m_detail.m_group.name = self.group.attrib['name']

    def statusAtrib(self):
        self.modelObject.m_detail.m_status.battery = self.status.attrib['battery']
    
    def trackAtrib(self):
        self.modelObject.m_detail.m_track.course = self.track.attrib['course']
        self.modelObject.m_detail.m_track.speed = self.track.attrib['speed']
    
    def returnModelObject(self):
        return self.modelObject