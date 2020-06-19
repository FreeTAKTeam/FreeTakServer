from logging.handlers import RotatingFileHandler
import logging
from configuration.LoggingConstants import LoggingConstants
import sys

loggingConstants = LoggingConstants()

class SendDataController:

    def __init__(self):
        
        log_format = logging.Formatter(loggingConstants.LOGFORMAT)
        self.logger = logging.getLogger(loggingConstants.LOGNAME)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.newHandler(loggingConstants.DEBUGLOG, logging.DEBUG, log_format))
        self.logger.addHandler(self.newHandler(loggingConstants.WARNINGLOG, logging.WARNING, log_format))
        self.logger.addHandler(self.newHandler(loggingConstants.INFOLOG, logging.INFO, log_format))
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(log_format)
        console.setLevel(logging.DEBUG)
        self.logger.addHandler(console)

    
    def newHandler(self, filename, log_level, log_format):
        handler = RotatingFileHandler(
            filename,
            maxBytes=loggingConstants.MAXFILESIZE,
            backupCount=loggingConstants.BACKUPCOUNT
        )
        handler.setFormatter(log_format)
        handler.setLevel(log_level)
        return handler

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
                            print(e)
                            break
                    else:
                        break
        except Exception as e:
            self.logger.error(loggingConstants.SENDDATACONTROLLERSENDDATAINQUEUEERROR+str(e))