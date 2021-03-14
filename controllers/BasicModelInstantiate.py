import xml.etree.ElementTree as etree


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
        self.modelObject.Point.lat = self.point.attrib['lat']
        self.modelObject.Point.lat = self.point.attrib['lon']
        self.modelObject.Point.lat = self.point.attrib['hae']
        self.modelObject.Point.lat = self.point.attrib['ce']
        self.modelObject.Point.lat = self.point.attrib['le']

    def takvAtrib(self):
        self.modelObject.detail.Takv.os = self.takv.attrib['os']
        self.modelObject.detail.Takv.device = self.takv.attrib['device']
        self.modelObject.detail.Takv.platform = self.takv.attrib['platform']
        self.modelObject.detail.Takv.version = self.takv.attrib['version']

    def contactAtrib(self):
        try:
            self.modelObject.detail.Contact.endpoint = self.contact.attrib['endpoint']
        except:
            pass
        try:
            self.modelObject.detail.Contact.callsign = self.contact.attrib['callsign']
        except:
            pass
    def uidAtrib(self):
        self.modelObject.detail.Uid.Droid = self.uid.attrib['Droid']
    
    def precisionlocationAtrib(self):
        try:
            self.modelObject.detail.precisionlocation.altsrc = self.precisionlocation.attrib['altsrc']
        except:
            pass
        try:
            self.modelObject.detail.precisionlocation.geopointsrc = self.precisionlocation.attrib['geopointsrc']
        except:
            pass
    def groupAtrib(self):
        self.modelObject.detail.Group.role = self.group.attrib['role']
        self.modelObject.detail.Group.name = self.group.attrib['name']

    def statusAtrib(self):
        self.modelObject.detail.Status.battery = self.status.attrib['battery']
    
    def trackAtrib(self):
        self.modelObject.detail.Track.course = self.track.attrib['course']
        self.modelObject.detail.Track.speed = self.track.attrib['speed']
    
    def linkAtrib(self):
        try:
            self.modelObject.detail.link.uid = self.link.attrib['uid']
        except:
            pass
        try:
            self.modelObject.detail.link.type = self.link.attrib['type']
        except:
            pass
        try:
            self.modelObject.detail.link.relation = self.link.attrib['relation']
        except:
            pass
    def emergencyAtrib(self):
        try:
            self.modelObject.detail.emergency.type = self.emergency.attrib['type']
        except:
            pass
        
        try:
            self.modelObject.detail.emergency.cancel = self.emergency.attrib['cancel']
        except:
            pass 
    
    def returnModelObject(self):
        return self.modelObject
