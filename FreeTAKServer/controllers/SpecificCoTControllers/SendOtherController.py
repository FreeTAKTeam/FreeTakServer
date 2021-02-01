from lxml import etree
from FreeTAKServer.model.SpecificCoT.SendOther import SendOther
from .SendCoTAbstractController import SendCoTAbstractController
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendOtherController").getLogger()
class SendOtherController(SendCoTAbstractController):
    def __init__(self, RawCoT=None):
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
                self.fill_object(self.object, tempObject, RawCoT)
                try:
                    object = self.getObject()

                except Exception as e:
                    logger.error("there has been an exception getting object " + str(e))
                self.Object.setXmlString(xml)
            else:
                pass
        except Exception as e:
            logger.error("there has been an exception in the creation of an"
                         "Other object " + str(e))
    #this function modifies the CoT so only the marti and point tags are present
    def filter_CoT(self, event):
        try:
            outputEvent = etree.fromstring(event)
            tempDetail = outputEvent.find('detail')
            outputEvent.remove(tempDetail)
            detail = etree.fromstring(event).find('detail')
            try:
                marti = detail.find('marti')
                outputDetail = etree.SubElement(outputEvent, 'detail')
                outputDetail.append(marti)
                print('dest client found')
                self.object.martiPresent = True
            except:
                etree.SubElement(outputEvent, 'detail')
                print('no dest client found')

            return outputEvent
        except Exception as e:
            print('exception filtering CoT ' + str(e))