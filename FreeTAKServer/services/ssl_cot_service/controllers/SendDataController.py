from typing import Dict
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.RawCoT import RawCoT

loggingConstants = LoggingConstants(log_name="FTS_SendDataController")
logger = CreateLoggerController(
    "FTS_SendDataController", logging_constants=loggingConstants
).getLogger()
import copy

# TODO: the part handling new connection from seperate process needs to be cleaned up


class SendDataController:
    def __init__(self):
        pass

    def sendDataInQueue(
        self,
        sender,
        processedCoT,
        clientInformationQueue,
        shareDataPipe=None,
        messages_to_core_count=0,
    ):
        self.messages_to_core_count = messages_to_core_count
        try:
            pass
            # print('sending data to fts client' + str(processedCoT.xmlString))
        except Exception as e:
            print(e)
        try:
            if processedCoT.type == "GeoChat":
                self.returnData = self.geochat_sending(
                    clientInformationQueue, processedCoT, sender, shareDataPipe
                )
                return self.returnData

            elif sender == processedCoT:
                for user_id, client in clientInformationQueue.items():
                    try:
                        if user_id != processedCoT.modelObject.uid:
                            user = client[1]
                            sock = client[0]

                            # send new client data to existing clients
                            sock.send(processedCoT.idData.encode())

                            # send existing client data to new client
                            sender.socket.send(user.m_presence.xmlString.encode())
                            # this is a special case which is identified
                            # by the server due to the list contents
                            # being within a list
                    except Exception as e:
                        logger.error(
                            "error in sending connection data "
                            + str(processedCoT.idData)
                        )
                copiedProcessedCoTObject = copy.deepcopy(processedCoT)
                copiedProcessedCoTObject.idData = (
                    copiedProcessedCoTObject.idData.encode()
                )
                self.messages_to_core_count += 1
                shareDataPipe.put([copiedProcessedCoTObject])
                return 1

            elif self.has_valid_marti(
                processedCoT
            ):  # this needs to check that val is greater than one because parsing automatically adds 1 dest value
                self.returnData = self.send_to_specific_client(
                    clientInformationQueue, processedCoT, sender, shareDataPipe
                )
                return self.returnData

            else:
                self.returnData = self.send_to_all(
                    clientInformationQueue, processedCoT, sender, shareDataPipe
                )
                return self.returnData

        except Exception as e:
            logger.error(
                loggingConstants.SENDDATACONTROLLERSENDDATAINQUEUEERROR + str(e)
            )
            return Exception(e)

    def send_to_specific_client(
        self, clientInformationQueue, processedCoT, sender, shareDataPipe
    ):
        try:
            dests = [
                dest.callsign for dest in processedCoT.modelObject.detail.marti.dest
            ]
            if not self.has_valid_marti(processedCoT) and not (
                hasattr(processedCoT.modelObject.detail, "_chat")
                and processedCoT.modelObject.detail._chat.chatgrp.uid1
                != "All Chat Rooms"
            ):
                # print('marti not present')
                return self.send_to_all(
                    clientInformationQueue, processedCoT, sender, shareDataPipe
                )
            elif dests == [None] or dests == [None, None]:
                return self.send_to_all(
                    clientInformationQueue, processedCoT, sender, shareDataPipe
                )
            else:
                # print('marti present')
                for dest in dests:
                    try:
                        for client_id, client in clientInformationQueue.items():
                            if (
                                client[1].m_presence.modelObject.detail.contact.callsign
                                == dest
                            ):
                                sock = client[0]
                                try:
                                    sock.send(processedCoT.xmlString)
                                    logger.info(
                                        str(processedCoT.xmlString)
                                        + " sent to client "
                                        + client_id
                                    )
                                except Exception as e:
                                    logger.error(
                                        "error sending data with marti to client data "
                                        + str(processedCoT.xmlString)
                                        + "error is "
                                        + str(e)
                                    )
                                    return (-1, client[1])
                            else:
                                continue
                    except Exception as e:
                        logger.error(
                            "error sending data with marti to client within if data is "
                            + str(processedCoT.xmlString)
                            + "error is "
                            + str(e)
                        )
                        return -1
                if shareDataPipe != None:
                    processedCoT.clientInformation = None
                    self.messages_to_core_count += 1
                    shareDataPipe.put(processedCoT)
                else:
                    pass
                return 1
        except Exception as e:
            logger.error("error in send data to specific client " + str(e))
            return -1

    def send_to_all(self, clientInformationQueue, processedCoT, sender, shareDataPipe):
        try:
            for client_id, client in clientInformationQueue.items():
                if (
                    processedCoT.type != "TakPong"
                    and hasattr(sender, "user_id")
                    and client_id == sender.user_id
                ):
                    continue
                sock = client[0]
                try:
                    if hasattr(processedCoT, "xmlString"):
                        # print('sending to all ' + str(processedCoT.xmlString))
                        try:
                            sock.send(processedCoT.xmlString)
                        except TypeError:
                            sock.send(processedCoT.xmlString.encode())
                        logger.info(
                            str(processedCoT.xmlString) + " sent to client " + client_id
                        )
                    else:
                        try:
                            sock.send(processedCoT.idData)
                        except TypeError:
                            sock.send(processedCoT.idData.encode())
                        logger.info(
                            str(processedCoT.idData) + " sent to client " + client_id
                        )
                except Exception as e:
                    logger.error("error in sending of data " + str(e))
                    return (-1, client[1])
            if shareDataPipe != None:
                processedCoT.clientInformation = None
                self.messages_to_core_count += 1
                shareDataPipe.put(processedCoT)
            else:
                pass
            return 1
        except Exception as e:
            import traceback

            logger.error(
                "error in send to all "
                + str(e)
                + str(traceback.format_exc())
                + " "
                + str(clientInformationQueue)
            )
            raise Exception(e)

    def geochat_sending(
        self,
        clientInformationQueue: Dict[str, list],
        processedCoT: RawCoT,
        sender,
        shareDataPipe,
    ):
        try:
            if processedCoT.modelObject.detail._chat.chatgrp.uid1 == "All Chat Rooms":
                return self.send_to_all(
                    clientInformationQueue, processedCoT, sender, shareDataPipe
                )

            else:
                for uid, client in clientInformationQueue.items():
                    try:
                        if uid == processedCoT.modelObject.detail._chat.chatgrp.uid1:
                            sock = client[0]
                            try:
                                sock.send(processedCoT.xmlString)
                            except Exception as e:
                                logger.error(
                                    "error sending data with marti to client data "
                                    + str(processedCoT.xmlString)
                                    + "error is "
                                    + str(e)
                                )
                                return (-1, client[1])
                        else:
                            continue
                    except Exception as e:
                        logger.error(
                            "error sending data with marti to client within if data is "
                            + str(processedCoT.xmlString)
                            + "error is "
                            + str(e)
                        )
                        return -1
                logger.info("CoT sent " + str(processedCoT.modelObject.uid))
                if shareDataPipe != None:
                    processedCoT.clientInformation = None
                    if hasattr(self, "messages_to_core_count"):
                        self.messages_to_core_count += 1
                    shareDataPipe.put(processedCoT)
                else:
                    pass
                return 1
        except Exception as e:
            logger.error("there has been an exception in sending geochat " + str(e))

    def has_valid_marti(self, message):
        if hasattr(message, "modelObject"):
            if (
                hasattr(message.modelObject.detail, "marti")
                and len(message.modelObject.detail.marti.dest) > 1
            ):
                return True
            elif hasattr(message.modelObject.detail, "marti"):
                if (
                    message.modelObject.detail.marti.dest[0].callsign != None
                    and message.modelObject.detail.marti.dest[0].callsign != ""
                ):
                    return True
            elif (
                hasattr(message.modelObject.detail, "_chat")
                and message.modelObject.detail._chat.chatgrp.uid1 != "All Chat Rooms"
            ):
                return True
            return False
