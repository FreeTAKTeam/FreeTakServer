import xml.etree.ElementTree as etree
from FreeTAKServer.controllers.model.Event import Event

class BasicModelInstantiate:
    def __init__(self, root, modelObject):
        try:
            self.modelObject = modelObject
            root = root.encode()
            self.event = etree.XML(root)
            self.establishVariables()
            self.eventAtrib()
            self.pointAtrib()
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
        self.link = self.detail.find('link')
        self.emergency = self.detail.find('emergency')

    def eventAtrib(self):
        self.modelObject.uid = self.event.attrib['uid']
        self.modelObject.type = self.event.attrib['type']
        self.modelObject.how = self.event.attrib['how']

    def pointAtrib(self):
        self.modelObject.m_Point.lat = self.point.attrib['lat']
        self.modelObject.m_Point.lat = self.point.attrib['lon']
        self.modelObject.m_Point.lat = self.point.attrib['hae']
        self.modelObject.m_Point.lat = self.point.attrib['ce']
        self.modelObject.m_Point.lat = self.point.attrib['le']

    def takvAtrib(self):
        self.modelObject.m_detail.m_Takv.os = self.takv.attrib['os']
        self.modelObject.m_detail.m_Takv.device = self.takv.attrib['device']
        self.modelObject.m_detail.m_Takv.platform = self.takv.attrib['platform']
        self.modelObject.m_detail.m_Takv.version = self.takv.attrib['version']

    def contactAtrib(self):
        try:
            self.modelObject.m_detail.m_Contact.endpoint = self.contact.attrib['endpoint']
        except:
            pass
        try:
            self.modelObject.m_detail.m_Contact.callsign = self.contact.attrib['callsign']
        except:
            pass
    def uidAtrib(self):
        self.modelObject.m_detail.m_Uid.Droid = self.uid.attrib['Droid']
    
    def precisionlocationAtrib(self):
        try:
            self.modelObject.m_detail.m_precisionlocation.altsrc = self.precisionlocation.attrib['altsrc']
        except:
            pass
        try:
            self.modelObject.m_detail.m_precisionlocation.geopointsrc = self.precisionlocation.attrib['geopointsrc']
        except:
            pass
    def groupAtrib(self):
        self.modelObject.m_detail.m_Group.role = self.group.attrib['role']
        self.modelObject.m_detail.m_Group.name = self.group.attrib['name']

    def statusAtrib(self):
        self.modelObject.m_detail.m_Status.battery = self.status.attrib['battery']
    
    def trackAtrib(self):
        self.modelObject.m_detail.m_Track.course = self.track.attrib['course']
        self.modelObject.m_detail.m_Track.speed = self.track.attrib['speed']
    
    def linkAtrib(self):
        try:
            self.modelObject.m_detail.m_link.uid = self.link.attrib['uid']
        except:
            pass
        try:
            self.modelObject.m_detail.m_link.type = self.link.attrib['type']
        except:
            pass
        try:
            self.modelObject.m_detail.m_link.relation = self.link.attrib['relation']
        except:
            pass
    def emergencyAtrib(self):
        try:
            self.modelObject.m_detail.m_emergency.type = self.emergency.attrib['type']
        except:
            pass
        
        try:
            self.modelObject.m_detail.m_emergency.cancel = self.emergency.attrib['cancel']
        except:
            pass 
    
    def returnModelObject(self):
        return self.modelObject
