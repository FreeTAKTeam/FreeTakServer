from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from defusedxml import ElementTree as etree
from FreeTAKServer.model.ExCheck.templateInstanceContents import templateInstanceContents
import hashlib
import os
from FreeTAKServer.model.ExCheck.template import template
from FreeTAKServer.model.ExCheck.templateInstance import templateInstance

class templateSerializer:
    def __init__(self, templateFile = None):
        self.templatedata = templateFile

    def convert_template_to_object(self):
        templateObject = templateInstanceContents()
        templateDetails = etree.fromstring(self.templatedata)
        templateDetails = templateDetails.find('checklistDetails')
        templateObject.settimestamp()
        templateObject.data.setkeywords(name=templateDetails.find('name').text, description=templateDetails.find('description').text, callsign=templateDetails.find('creatorCallsign').text)
        templateObject.setcreatoruid(templateDetails.find('creatorUid').text)
        templateObject.data.setname(templateDetails.find('uid').text)
        templateObject.data.setuid(templateDetails.find('uid').text)
        templateObject.data.sethash(str(hashlib.sha256(str(self.templatedata).encode()).hexdigest()))
        templateObject.data.setsize(len(self.templatedata))
        templateObject.data.setfilename()
        # TODO: include in DB the submitting user
        templateObject.data.setsubmitter('test')
        templateObject.data.settool('ExCheck')
        templateObject.data.setsubmissionTime()
        return templateObject

    def convert_DB_to_object(self, DBObject):
        templateObject = templateInstanceContents()
        templateObject.setcreatoruid(DBObject.creatorUid)
        templateObject.data.setname(DBObject.data.uid)
        templateObject.data.setuid(DBObject.data.uid)
        templateObject.data.sethash(DBObject.data.hash)
        templateObject.data.setsize(DBObject.data.size)
        templateObject.data.setkeywords(name=DBObject.data.keywords.name, description=DBObject.data.keywords.description, callsign=DBObject.data.keywords.callsign)
        templateObject.data.setfilename()
        # TODO: include in DB the submitting user
        templateObject.data.setsubmitter('test')
        templateObject.data.settool('ExCheck')
        templateObject.data.setsubmissionTime()
        return templateObject

    def create_DB_object(self, templateObject):
        self.DataBase = DatabaseController()
        self.DataBase.create_ExCheck(templateObject)
        self.DataBase.shutdown_Connection()

    def convert_object_to_json(self, DBObject):
        templateJsonMessage = template()
        templateJsonMessage.data.append(templateInstance())
        for content in DBObject:
            contentobj = self.convert_DB_to_object(content)
            contentobj.data = vars(contentobj.data)
            templateJsonMessage.data[0].contents.append(vars(contentobj))
        y = vars(templateJsonMessage)
        y['data'][0] = vars(y['data'][0])
        return y

if __name__ == "__main__":
    serializer = templateSerializer(r'C:\Users\natha\PycharmProjects\InDev\FreeTAKServerParent\FreeTAKServer\Tests\ExCheckTesting\excheckxmi\13c3e6b4-c25a-40d3-9938-0d32a6c09e45.xml')
    obj1 = serializer.convert_template_to_object()
    #obj2 = serializer.create_DB_object(obj1)
    #serializer.convert_object_to_json(DatabaseController().query_ExCheck())