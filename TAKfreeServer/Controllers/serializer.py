import xml.etree.ElementTree as ET


class Serializer:
    def __init__(self):
        self.xmlheader = '<?xml version="1.0" encoding="UTF-8" standalone="true"?>'

    def serializerRoot(self, object):
        root = ET.Element('event')
        for key, value in vars(object).items():
            if hasattr(value, '__dict__') == True and isinstance(value, type) == False:
                self.serializerSub(root, key, value)
            else:
                root.set(key, str(value))
        return self.xmlheader + ET.tostring(root).decode()

    def serializerSub(self, parent, tag, object):
        tag = ET.SubElement(parent, tag)
        for key, value in vars(object).items():
            if hasattr(value, '__dict__') == True and isinstance(value, type) == False:
                self.serializerSub(tag, key, value)
            else:
                tag.set(key, str(value))
