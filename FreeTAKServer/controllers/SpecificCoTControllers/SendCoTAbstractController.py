from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.FTSModel.Event import Event as event
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from abc import ABC
from FreeTAKServer.controllers.serializers import xml_serializer

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendCoTAbstract").getLogger()

class SendCoTAbstractController(ABC):
    Event = event
    def __init__(self, object):
        pass

    def fill_object(self, object, tempObject, RawCoT, addToDB = MainConfig.SaveCoTToDB):
        try:
            object.modelObject = self.create_model_object(tempObject, RawCoT.xmlString)

        except Exception as e:
            if tempObject.type != "other":
                self.handel_serialization_exception(object, RawCoT)
                logger.error('an undocumented CoT has been sent returning the error ' + str(e) + ' please post this as an issue on the FTS git so we can document and fix it')
                return 1
            else:
                logger.warning('there has been an exception in the creation of the model object ' + str(e))
                return -1

        try:
            object.xmlString = self.create_xml_string(object.modelObject)
        except Exception as e:
            logger.warning('there has been an exception in the creation of a xmlString ' + str(e))
        try:
            if addToDB == True:
                RawCoT.dbController.create_CoT(object.modelObject)
            else:
                pass
        except Exception as e:
            logger.warning('there has been an exception in the creation of a database instance of this object ' + str(e))
            raise Exception(e)
        self.setObject(object)

    def create_model_object(self, tempObject, xmlString):
        """
        this function takes an empty model object and xml as arguments and then calls the serializer within the xmlcotcontroller
        module which returns a model object occupied with all the data from the CoT
        """
        from FreeTAKServer.controllers.XMLCoTController import XMLCoTController

        modelInstance = xml_serializer.XmlSerializer().from_format_to_fts_object(xmlString, tempObject)
        return modelInstance
    def create_xml_string(self, modelObject):
        """
        this function calls the model to xml serializer within XMLCoTController
        with an instantiated model object supplied in the function argument
        """
        from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
        try:
            xml = XMLCoTController().serialize_model_to_CoT(modelObject, 'event')
            return xml
        except Exception as e:
            logger.error('there has been an exception in the creation of the xml string ' +str(e))
            return -1

    def handel_serialization_exception(self, object, RawCoT):
        """
        this function will handle any exception thrown in the process of serialization of an xml CoT to it's respective model object
        by processing it as an Other type
        """
        from FreeTAKServer.controllers.SpecificCoTControllers.SendOtherController import SendOtherController
        object = SendOtherController(RawCoT).getObject()
        object.clientInformation = RawCoT.clientInformation
        self.setObject(object)


    def setObject(self, object):
        self.Object = object

    def getObject(self):
        return self.Object

    def reloadXmlString(self):
        self.Object.xmlString = self.create_xml_string(self.Object.modelObject)