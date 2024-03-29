#######################################################
#
# ClientReceptionHandler.py
# Python implementation of the Class ClientReceptionHandler
# Generated by Enterprise Architect
# Created on:      19-May-2020 7:17:21 PM
# Original author: Natha Paquette
#
#######################################################
import time
import socket
import errno
import copy
import re

from FreeTAKServer.core.configuration.MainConfig import MainConfig
from ..configuration.tcp_cot_service_constants import DATA_RECEPTION_BUFFER_SIZE
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from defusedxml import ElementTree as etree

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

loggingConstants = LoggingConstants(log_name="FTS_ClientReceptionHandler")
logger = CreateLoggerController("FTS_ClientReceptionHandler", logging_constants=loggingConstants).getLogger()
from FreeTAKServer.core.configuration.ClientReceptionLoggingConstants import ClientReceptionLoggingConstants

loggingConstants = ClientReceptionLoggingConstants()
BUFF_SIZE = DATA_RECEPTION_BUFFER_SIZE

class ClientReceptionHandler:
    def __init__(self):
        self.dataPipe = []
        self.socketCount = 0

    def startup(self, clientInformationArray):
        try:
            self.clientInformationArray = clientInformationArray  # create copy of client information array so it cant be changed during iteration
            '''logger.propagate = False
            logger.info(loggingConstants.CLIENTRECEPTIONHANDLERSTART)
            logger.propagate = True'''
            output = self.monitorForData(self.dataPipe)
            if output == 1:
                if len(self.dataPipe)>0: logger.debug("returning data array %s", str(self.dataPipe))
                return self.dataPipe
            else:
                return -1
            '''
            time.sleep(600)
            # temporarily remove due to being unnecessary and excessively flooding logs
            logger.info('the number of threads is ' + str(threading.active_count()) + ' monitor event process alive is ' + str(monitorEventProcess.is_alive()) +
                        ' return data to Orchestrator process alive is ' + str(monitorForData.is_alive()))
            '''
        except Exception as e:
            logger.error(loggingConstants.CLIENTRECEPTIONHANDLERSTARTUPERROR + str(e))

    def monitorForData(self, queue):
        '''
        updated receive all
        '''
        try:
            keys = copy.deepcopy(list(self.clientInformationArray.keys()))  # this prevents changes to the clientInformationArray from having any severe effects on this method
            for user_id in keys:
                sock = self.clientInformationArray[user_id][0]
                client = user_id
                #client = self.clientInformationArray[user_id][1]
                try:
                    sock.settimeout(0.001)
                    try:
                        xmlstring = self.recv_until(sock).decode()
                        logger.debug("received raw data %s", str(xmlstring))
                        if xmlstring == b'' or xmlstring == '' or xmlstring is None: 
                            #xmlstring = self.validate_client_disconnect(queue, sock, client)
                            #if xmlstring is None:
                            #    continue
                            self.returnReceivedData(client, b'', queue)
                            continue
                        xmlstring = "<multiEvent>" + xmlstring + "</multiEvent>"  # convert to xmlstring wrapped by multiEvent tags
                        xmlstring = re.sub(r"<\?xml.*?\?>", '', xmlstring)  # replace xml definition tag with empty string as it breaks serilization
                        logger.debug("data after xmltag substitution: %s", xmlstring)
                        events = etree.fromstring(xmlstring)  # serialize to object
                        for event in events.findall('event'):
                            event_str = etree.tostring(event)
                            logger.debug("received: %s from %s", event_str, client)
                            self.returnReceivedData(client, etree.tostring(event), queue)  # send each instance of event to the core
                    except socket.timeout:
                        continue
                    except BrokenPipeError as ex:
                        logger.debug("disconnecting client %s due to broken pipe", client)
                        self.returnReceivedData(client, b'', queue)
                        continue
                    except ConnectionAbortedError as ex:
                        logger.debug("disconnecting client %s due to connection aborted", client)
                        self.returnReceivedData(client, b'', queue)
                        continue
                    except ConnectionResetError as ex:
                        logger.debug("disconnecting client %s due to connection reset", client)
                        self.returnReceivedData(client, b'', queue)
                        continue
                    except Exception as ex:
                        import traceback
                        if hasattr(ex, "errno") and ex.errno == errno.EWOULDBLOCK:  # this prevents errno 11 from spontanieously disconnecting clients due to the socket blocking set to 0
                            logger.debug("EWOULDBLOCK error passed " + str(ex))
                            continue
                        logger.error(
                            "Exception other than broken pipe in monitor for data function " + str(ex) + ''.join(traceback.format_exception(None, ex, ex.__traceback__)))
                        self.returnReceivedData(client, b'', queue)
                        continue

                except Exception as ex:
                    logger.error(loggingConstants.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORD + str(ex))
                    self.returnReceivedData(client, b'', queue)
                    # return -1 commented out so entire run isn't stopped because of one disconnect
            return 1
        except Exception as ex:
            logger.error('exception in monitor for data ' + str(ex))
            return -1

    def validate_client_disconnect(self, queue, sock, client):
        """ensure that the client is correctly disconnected

        Args:
            queue (_type_): _description_
            sock (_type_): _description_
            client (_type_): _description_

        Returns:
            _type_: _description_
        """
        for _ in range(10):
            xmlstring = self.recv_until(sock).decode()
            if xmlstring != b'' or xmlstring != '' or xmlstring is not None:
                return xmlstring
        logger.debug("empty string sent from %s, standard disconnect", client)
        self.returnReceivedData(client, b'', queue)
        return None
    
    def returnReceivedData(self, clientInformation, data, queue):
        try:
            from FreeTAKServer.model.RawCoT import RawCoT
            RawCoT = RawCoT()
            RawCoT.clientInformation = clientInformation
            RawCoT.xmlString = data.replace(b'\n', b'')  # replace all newlines with empty
            self.dataPipe.append(RawCoT)
            logger.debug("data received "+ str(data))
            return 1
        except Exception as e:
            logger.error(loggingConstants.CLIENTRECEPTIONHANDLERRETURNRECEIVEDDATAERROR + str(e))
            return -1

    def recv_until(self, client):
        start_receive_time = time.time()
        message = client.recv(BUFF_SIZE)
        while time.time() - start_receive_time <= config.MaxReceptionTime:
            try:
                message = message + client.recv(BUFF_SIZE)
            except Exception as e:
                break
        return message