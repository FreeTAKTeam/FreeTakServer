import datetime as dt
import uuid
import xml.etree.ElementTree as ET
import socket
import logging

logger = logging.getLogger("django")

ID = {
    "pending": "p",
    "unknown": "u",
    "assumed-friend": "a",
    "friend": "f",
    "neutral": "n",
    "suspect": "s",
    "hostile": "h",
    "joker": "j",
    "faker": "f",
    "none": "o",
    "other": "x"
}
DIM = {
    "space": "P",
    "air": "A",
    "land-unit": "G",
    "land-equipment": "G",
    "land-installation": "G",
    "sea-surface": "S",
    "sea-subsurface": "U",
    "subsurface": "U",
    "other": "X"
}

DATETIME_FMT = "%Y-%m-%dT%H:%M:%SZ"

class CursorOnTarget:

    def atoms():
        timer = dt.datetime
        now = timer.utcnow()
        zulu = now.strftime(DATETIME_FMT)
        stale_part = now.minute + 1
        if stale_part > 59:
            stale_part = stale_part - 60
        stale_now = now.replace(minute=stale_part)
        stale = stale_now.strftime(DATETIME_FMT)
        cot_xml = "<?xml version='1.0' encoding='UTF-8' standalone='yes'?><event version='2.0' uid='deccf9b1-ee37-4205-a235-a6d527fc7c24' type='a-f-G' time='{0}' start='{0}' stale='{1}' how='h-g-i-g-o'><point lat='44.2198868' lon='-66.1382602' hae='-13.62' ce='9999999.0' le='9999999.0' /><detail><link uid='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' production_time='2020-02-01T18:48:14Z' relation='p-p' type='a-f-G' parent_callsign='Eliopoli HQ'/><archive/><usericon iconsetpath='COT_MAPPING_2525B/a-f/a-f-G'/><precisionlocation altsrc='DTED0'/><contact callsign='F.1.184814'/></detail></event>".format(zulu, stale)
        f = open("xmlfile.xml", "a")
        f.truncate()
        f.write(cot_xml)
        f.close()
        print(cot_xml)
        print('running')
        return cot_xml

    def pushUDP(__self, ip_address, port, cot_xml):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sent = sock.sendto(cot_xml, (ip_address, port))
            return sent

    def pushTCP(__self, ip_address, port, cot_xml):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn = sock.connect((ip_address, port))
                return sock.send(cot_xml)

class CoT:
    """The Cursor-On-Target (CoT) Event data model defines an XML data schema for
    exchanging time sensitive position of moving objects, or "what", "when", and
    "where" (WWW) information, between systems.
    """
    Identity = "unknow" 
     # Identity getter 
    def getIdentity(self): 
        return self.Identity 
 
     # Identity setter 
    def setIdentity(Identity=0):  
        self.Identity=Identity 
     
    dimension = "land-unit" 
     # dimension getter 
    def getdimension(self): 
        return self.dimension 
 
     # dimension setter 
    def setdimension(dimension=0):  
        self.dimension=dimension 
     
    entity = "military" 
     # entity getter 
    def getentity(self): 
        return self.entity 
 
     # entity setter 
    def setentity(entity=0):  
        self.entity=entity 
     
    type = "E-V-A-T" 
     # type getter 
    def gettype(self): 
        return self.type 
 
     # type setter 
    def settype(type=0):  
        self.type=type 
     
    lat = "" 
     # lat getter 
    def getlat(self): 
        return self.lat 
 
     # lat setter 
    def setlat(lat=0):  
        self.lat=lat 
     
    lon = "" 
     # lon getter 
    def getlon(self): 
        return self.lon 
 
     # lon setter 
    def setlon(lon=0):  
        self.lon=lon 
     
    uid = "" 
     # uid getter 
    def getuid(self): 
        return self.uid 
 
     # uid setter 
    def setuid(uid=0):  
        self.uid=uid 
     
