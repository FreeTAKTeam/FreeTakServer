from defusedxml import ElementTree as etree
from FreeTAKServer.model.SpecificCoT.SendOther import SendOther
from FreeTAKServer.controllers.SpecificCoTControllers.SendCoTAbstractController import SendCoTAbstractController
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendOtherController").getLogger()
class SendOtherController(SendCoTAbstractController):
    def __init__(self, RawCoT=None, addToDB = MainConfig.SaveCoTToDB):
        if type(RawCoT != bytes):
            pass
        else:
            RawCoT.xmlString.encode()
        try:
            tempObject = super().Event.Other()
            self.object = SendOther()
            if RawCoT is not None:
                xml = RawCoT.xmlString
                RawCoT.xmlString = etree.tostring(self.filter_CoT(xml))
                self.fill_object(self.object, tempObject, RawCoT, addToDB=addToDB)
                try:
                    object = self.getObject()

                except Exception as e:
                    logger.error("there has been an exception getting object " + str(e))
                self.Object.setXmlString(xml)
            else:
                pass
        except Exception as e:
            print("exception"+str(e))
            logger.error("there has been an exception in the creation of an"
                         "Other object " + str(e))
    #this function modifies the CoT so only the marti and point tags are present
    def filter_CoT(self, event):
        try:
            from xml.etree.ElementTree import Element
            outputEvent = etree.fromstring(event)
            tempDetail = outputEvent.find('detail')
            outputEvent.remove(tempDetail)
            detail = etree.fromstring(event).find('detail')
            try:
                marti = detail.find('marti')
                outputDetail = Element('detail')
                outputDetail.append(marti)
                outputEvent.append(outputDetail)
                print('dest client found')
                self.object.martiPresent = True
            except Exception as e:
                outputDetail = Element('detail')
                outputEvent.append(outputDetail)
                print('no dest client found')

            return outputEvent
        except Exception as e:
            print('exception filtering CoT ' + str(e))
