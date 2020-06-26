from logging.handlers import RotatingFileHandler
import logging
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
import sys
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendDataController").getLogger()


class SendDataController:

    def __init__(self):
        pass
    def sendDataInQueue(self, sender, processedCoT, clientInformationQueue):
        try:
            try:
                if processedCoT.modelObject.m_detail.Marti.m_Dest.callsign != '':
                    for client in clientInformationQueue:
                        if client.modelObject.m_detail.m_Contact.callsign == processedCoT.modelObject.m_detail.Marti.m_Dest.callsign:
                            sock = client.socket
                            try:
                                sock.send(processedCoT.xmlString)
                            except:
                                break                    
                        else:
                            break
            except:
                pass
            
            if sender == processedCoT:
                for client in clientInformationQueue:
                    try:
                        sock = client.socket
                        sock.send(processedCoT.idData.encode())
                        sender.socket.send(client.idData.encode())
                    except:
                        break

            else:
                for client in clientInformationQueue:

                    if client != sender:
                        sock = client.socket
                        try:
                            sock.send(processedCoT.xmlString)
                        except Exception as e:
                            #print(e)
                            break
                    else:
                        break
        except Exception as e:
            logger.error(loggingConstants.SENDDATACONTROLLERSENDDATAINQUEUEERROR+str(e))