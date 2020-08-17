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
                if processedCoT.type == 'GeoChat':
                    return self.geochat_sending(clientInformationQueue, processedCoT, sender)
                else:
                    pass
            except:
                pass
            
            if sender == processedCoT:
                for client in clientInformationQueue:
                    try:
                        sock = client.socket
                        sock.send(processedCoT.idData.encode())
                        sender.socket.send(client.idData.encode())
                    except:
                        logger.error('error in sending connection data ' + str(processedCoT.idData))
                        return -1
                return 1


            else:
                return self.send_to_all(clientInformationQueue, processedCoT, sender)
        except Exception as e:
            logger.error(loggingConstants.SENDDATACONTROLLERSENDDATAINQUEUEERROR+str(e))
            return -1

    def send_to_all(self, clientInformationQueue, processedCoT, sender):
        for client in clientInformationQueue:
            if client != sender:

                sock = client.socket
                try:
                    print(processedCoT.xmlString)
                    sock.send(processedCoT.xmlString)
                except Exception as e:
                    logger.error('error in sending of data ' + str(processedCoT.xmlString))
                    return (-1, client)
            else:
                continue
        return 1

    def geochat_sending(self, clientInformationQueue, processedCoT, sender):
        if processedCoT.modelObject.detail._chat.chatgrp.uid1 == 'All Chat Rooms':
            return self.send_to_all(clientInformationQueue, processedCoT, sender)

        else:
            for client in clientInformationQueue:
                try:
                    if client.modelObject.uid == processedCoT.modelObject.detail._chat.chatgrp.uid1:
                        sock = client.socket
                        try:
                            sock.send(processedCoT.xmlString)
                        except Exception as e:
                            logger.error('error sending data with marti to client data ' + str(
                                processedCoT.xmlString) + 'error is ' + str(e))
                            return (-1, client)
                    else:
                        continue
                except Exception as e:
                    logger.error('error sending data with marti to client within if data is ' + str(
                        processedCoT.xmlString) + 'error is ' + str(e))
                    return -1
            return 1