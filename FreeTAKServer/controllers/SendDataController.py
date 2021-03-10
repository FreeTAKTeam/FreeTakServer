from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendDataController").getLogger()
import copy
#TODO: the part handling new connection from seperate process needs to be cleaned up

class SendDataController:

    def __init__(self):
        pass
    def sendDataInQueue(self, sender, processedCoT, clientInformationQueue, shareDataPipe = None):
        try:
            print('sending data to fts client' + str(processedCoT.xmlString))
        except Exception as e:
            print(e)
        try:
            if processedCoT.type == 'GeoChat':
                self.returnData = self.geochat_sending(clientInformationQueue, processedCoT, sender, shareDataPipe)
                return self.returnData
            elif sender == processedCoT:
                self.send_connection_data(clientInformationQueue, processedCoT, sender, shareDataPipe)
                return 1
            elif processedCoT.type == 'other':
                self.returnData = self.send_to_specific_client(clientInformationQueue, processedCoT, sender, shareDataPipe)
                return self.returnData
            else:
                self.returnData = self.send_to_all(clientInformationQueue, processedCoT, sender, shareDataPipe)
                return self.returnData
        except Exception as e:
            logger.error(loggingConstants.SENDDATACONTROLLERSENDDATAINQUEUEERROR+str(e))
            return -1

    def send_connection_data(self, clientInformationQueue, processedCoT, sender, shareDataPipe):
        for client in clientInformationQueue:
            try:
                sock = client.socket
                sock.send(processedCoT.idData.encode())
                sender.socket.send(client.idData.encode())
                # this is a special case which is identified
                # by the server due to the list contents
                # being within a list
            except Exception as e:
                logger.error('error in sending connection data ' + str(processedCoT.idData))
                pass
        copiedProcessedCoTObject = copy.deepcopy(processedCoT)
        copiedProcessedCoTObject.idData = copiedProcessedCoTObject.idData.encode()
        shareDataPipe.put([copiedProcessedCoTObject])

    def send_to_specific_client(self, clientInformationQueue, processedCoT, sender, shareDataPipe):
        try:
            if processedCoT.martiPresent == False:
                print('marti not present')
                return self.send_to_all(clientInformationQueue, processedCoT, sender, shareDataPipe)

            else:
                print('marti present')
                for dest in processedCoT.modelObject.detail.marti.dest:
                    try:
                        for client in clientInformationQueue:
                            if client.modelObject.detail.contact.callsign == dest.callsign:
                                print('client socket is ' + str(client.socket))
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
                if shareDataPipe != None:
                    processedCoT.clientInformation = None
                else:
                    pass
                return 1
        except Exception as e:
            logger.error('error in send data to specific client ' + str(e))
            return -1

    def send_to_all(self, clientInformationQueue, processedCoT, sender, shareDataPipe):
        try:
            for client in clientInformationQueue:
    
                sock = client.socket
                try:
                    if hasattr(processedCoT, 'xmlString'):
                        print('sending to all ' + str(processedCoT.xmlString))
                        sock.send(processedCoT.xmlString)
                    else:
                        sock.send(processedCoT.idData.encode())
                except Exception as e:
                    print(e)
                    logger.error('error in sending of data ' + str(processedCoT.xmlString))
                    return (-1, client)
            if shareDataPipe != None:
                processedCoT.clientInformation = None
                shareDataPipe.put(processedCoT)
            else:
                pass
            return 1
        except Exception as e:
            logger.error('error in send to all ' + str(e))
    def geochat_sending(self, clientInformationQueue, processedCoT, sender, shareDataPipe):
        try:
            if processedCoT.modelObject.detail._chat.chatgrp.uid1 == 'All Chat Rooms':
                return self.send_to_all(clientInformationQueue, processedCoT, sender, shareDataPipe)
    
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
                if shareDataPipe != None:
                    processedCoT.clientInformation = None
                else:
                    pass
                return 1
        except Exception as e:
            logger.error('there has been an exception in sending geochat ' + str(e))