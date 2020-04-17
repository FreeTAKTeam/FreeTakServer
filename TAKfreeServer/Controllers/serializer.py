import xml.etree.ElementTree as et
from Controllers.RequestCOTController import RequestCOTController
class Serializer:
    def __init__(self):
        self.xmlheader = "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"

    def serializerRoot(self, object):
        root = et.Element('event')
        for key, value in vars(object).items():
            if hasattr(value, '__dict__') == True and isinstance(value, type) == False:
                self.serializerSub(root, key, value)
            else:
                root.set(key, str(value))
        return self.xmlheader + et.tostring(root).decode()

    def serializerSub(self, parent, tag, object):
        tag = et.SubElement(parent, tag)
        for key, value in vars(object).items():
            if hasattr(value, '__dict__') == True and isinstance(value, type) == False:
                self.serializerSub(tag, key, value)
            else:
                tag.set(key, str(value))

