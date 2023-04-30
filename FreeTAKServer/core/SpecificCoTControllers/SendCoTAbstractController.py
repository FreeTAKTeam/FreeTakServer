from abc import ABC

from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.parsers.XMLCoTController import XMLCoTController
from FreeTAKServer.core.serializers import xml_serializer
from FreeTAKServer.model.FTSModel.Event import Event as event

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

loggingConstants = LoggingConstants(log_name="FTS_SendCoTAbstract")
logger = CreateLoggerController("FTS_SendCoTAbstract", logging_constants=loggingConstants).getLogger()

class SendCoTAbstractController(ABC):
    Event = event

    def fill_object(self, object, tempObject, RawCoT, addToDB=config.SaveCoTToDB):
        try:
            object.modelObject = self.create_model_object(tempObject, RawCoT.xmlString)

        except Exception as e:
            if tempObject.type != "other":
                self.handel_serialization_exception(object, RawCoT)
                logger.error('an undocumented CoT has been sent returning the error ' + str(
                    e) + ' please post this as an issue on the FTS git so we can document and fix it')
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
            print(e)
            logger.warning(
                'there has been an exception in the creation of a database instance of this object ' + str(e))
            raise Exception(e)
        logger.debug("serialized CoT "+str(RawCoT.xmlString)+" to type "+str(self))
        self.setObject(object)

    def create_model_object(self, tempObject, xmlString):
        """
        this function takes an empty model object and xml as arguments and then calls the serializer within the xmlcotcontroller
        module which returns a model object occupied with all the data from the CoT
        """
        modelInstance = xml_serializer.XmlSerializer().from_format_to_fts_object(xmlString, tempObject)
        return modelInstance

    def create_xml_string(self, modelObject):
        """
        this function calls the model to xml serializer within XMLCoTController
        with an instantiated model object supplied in the function argument
        """
        try:
            xml = XMLCoTController().serialize_model_to_CoT(modelObject, 'event')
            return xml
        except Exception as e:
            logger.error('there has been an exception in the creation of the xml string ' + str(e))
            return -1

    def handel_serialization_exception(self, object, RawCoT):
        """
        this function will handle any exception thrown in the process of serialization of an xml CoT to it's respective model object
        by processing it as an Other type
        """
        from FreeTAKServer.core.SpecificCoTControllers.SendOtherController import SendOtherController
        object = SendOtherController(RawCoT).getObject()
        object.clientInformation = RawCoT.clientInformation
        self.setObject(object)

    def setObject(self, object):
        self.Object = object

    def getObject(self):
        return self.Object

    def reloadXmlString(self):
        self.Object.xmlString = self.create_xml_string(self.Object.modelObject)
