from lxml import etree

class AbstractXMLSerializer:
    def __init__(self, xml):
        self.xml = xml

    def serializeFromXML(self):
        xml = etree.fromstring(self.xml)
        self.inTag(xml.text)
        for attribute in xml.attrib:
            self.attrib(attribute)
        for element in xml:
            self.tag(element)

    def tag(self, xml):
        pass

    def attrib(self, xml):
        pass

    def inTag(self, xml):
        pass