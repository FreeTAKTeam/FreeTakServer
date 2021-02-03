from abc import ABC


class SpecificCoTAbstract(ABC):
    def define_variables(self):
        self.type = None
        self.clientInformation = None
        self.modelObject = None
        self.xmlString = None

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def setXmlString(self, xmlString):
        self.xmlString = xmlString

    def getXmlString(self):
        return self.xmlString

    def setClientInformation(self, clientInformation):
        self.clientInformation = clientInformation

    def getClientInformation(self):
        return self.clientInformation

    def setModelObject(self, modelObject):
        self.modelObject = modelObject

    def getModelObject(self):
        return self.modelObject
