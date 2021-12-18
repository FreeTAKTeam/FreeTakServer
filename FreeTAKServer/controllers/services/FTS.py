import multiprocessing
import threading
import argparse
import linecache
import sys

from FreeTAKServer.controllers.CreateStartupFilesController import CreateStartupFilesController

CreateStartupFilesController()

from FreeTAKServer.model.User import User

from FreeTAKServer.controllers.services.TCPDataPackageService import TCPDataPackageService as TCPFlaskFunctions
from FreeTAKServer.controllers.services.SSLDataPackageService import SSLDataPackageService as SSLFlaskFunctions
from FreeTAKServer.controllers.configuration.OrchestratorConstants import OrchestratorConstants
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.services.RestAPI import RestAPI
from FreeTAKServer.model.ServiceObjects.FTS import FTS as FTSObj
from FreeTAKServer.model.SimpleClient import SimpleClient
from FreeTAKServer.controllers.configuration_wizard import ask_user_for_config
import time
from FreeTAKServer.controllers.AddDataToCoTList import AddDataToCoTList
from FreeTAKServer.model.FilterGroup import FilterGroup
from FreeTAKServer.controllers.services.SSLCoTServiceController import SSLCoTServiceController
from FreeTAKServer.controllers.services.TCPCoTServiceController import TCPCoTServiceController
from FreeTAKServer.controllers.services.federation.FederationClientService import FederationClientServiceController
from FreeTAKServer.controllers.services.federation.federation import FederationServerService
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.controllers.certificate_generation import AtakOfTheCerts
from multiprocessing import Queue
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from FreeTAKServer.model.SpecificCoT.Presence import Presence
from FreeTAKServer.model.Connection import Connection

from FreeTAKServer.model.Enumerations.connectionTypes import ConnectionTypes

loggingConstants = LoggingConstants(log_name="FTS_FTSCore")
logger = CreateLoggerController("FTS_FTSCore", logging_constants=loggingConstants).getLogger()

loggingConstants = LoggingConstants()


# noinspection PyUnresolvedReferences
class FTS:

    def __init__(self):
        self.CoTService = None
        self.TCPDataPackageService = None
        self.UserCommand = None
        self.killSwitch = False
        self.ReceiveConnectionsReset = None
        self.CoTPoisonPill = None
        self.core_tcp_user_queue_send = None
        self.SSLClientDataPipe = None
        self.user_dict = {}
        self.socketCount = 0
        self.pipeList = {}
        self.FilterGroup = FilterGroup()
        self.FTSServiceStartupConfigObject = FTSObj()
        self.dbController = DatabaseController()
        logger.propagate = True
        logger.info('something')

    def start_restAPI_service(self, StartupObjects):
        try:
            self.RestAPIPipe = Queue()
            restapicommandsthread = Queue()
            restapicommandsmain = Queue()
            self.RestAPICommandsFTS = QueueManager(restapicommandsmain, restapicommandsthread)
            RestAPICommandsFTS = QueueManager(restapicommandsthread, restapicommandsmain)
            self.receive_Rest_stopper = multiprocessing.Event()
            self.receive_Rest_stopper.clear()
            self.receive_Rest = threading.Thread(target=self.receive_Rest_commands, args=(self.receive_Rest_stopper,))
            self.RestAPIProcess = multiprocessing.Process(target=RestAPI().startup, args=(
            self.RestAPIPipe, RestAPICommandsFTS, StartupObjects.RestAPIService.RestAPIServiceIP,
            StartupObjects.RestAPIService.RestAPIServicePort, self.StartupTime))
            self.receive_Rest.start()
            self.RestAPIProcess.start()
            self.pipeList['restAPI'] = self.RestAPIPipe
            self.FilterGroup.sources.append(self.RestAPIPipe)
            return 1
        except Exception as e:
            logger.error('There has been an exception thrown in the startup of the restAPI service ' + str(e))
            return -1

    def stop_RestAPI_service(self):
        try:
            self.RestAPIProcess.terminate()
            self.RestAPIProcess.join()
            self.receive_Rest_stopper.set()
            self.receive_Rest.join()
        except Exception as e:
            logger.error('an exception has been thrown in RestAPI Startup ' + str(e))

    def start_CoT_service(self, FTSServiceStartupConfigObject):
        try:
            self.core_tcp_user_queue_send = Queue()
            self.service_tcp_user_queue_send = Queue()
            TCPCoTServiceThread = Queue()
            TCPCoTServiceFTS = Queue()
            self.TCPCoTService = QueueManager(TCPCoTServiceThread, TCPCoTServiceFTS)
            TCPCoTService = QueueManager(TCPCoTServiceFTS, TCPCoTServiceThread)
            print('event event about to be created')
            self.CoTPoisonPill = multiprocessing.Event()
            self.CoTPoisonPill.set()
            self.ReceiveConnectionsReset = multiprocessing.Event()
            self.CoTService = multiprocessing.Process(target=TCPCoTServiceController().start, args=(
            FTSServiceStartupConfigObject.CoTService.CoTServiceIP,
            FTSServiceStartupConfigObject.CoTService.CoTServicePort, self.CoTPoisonPill, self.service_tcp_user_queue_send,
            self.ReceiveConnectionsReset, TCPCoTService, self.core_tcp_user_queue_send))
            self.CoTService.start()
            self.pipeList['TCPCoTServiceFTSPipe'] = self.TCPCoTService
            self.FilterGroup.receivers.append(self.TCPCoTService)
            self.FilterGroup.sources.append(self.TCPCoTService)
            print('CoTService started')
            return 1
        except Exception as e:
            logger.error('an exception has been thrown in CoT service startup ' + str(e))
            return -1

    def stop_CoT_service(self):
        try:
            # self.ClientDataPipe.close()
            self.CoTPoisonPill.clear()

            time.sleep(1)
            if self.CoTService.is_alive():
                self.CoTService.terminate()
                self.CoTService.join()
            else:
                self.CoTService.join()

            self.FilterGroup.sources.remove(self.TCPCoTService)
            self.FilterGroup.receivers.remove(self.TCPCoTService)

        except Exception as e:
            logger.error("there's been an exception in the stopping of CoT Service " + str(e))
            return -1
        return 1

    def start_tcp_data_package_service(self, FTSServiceStartupConfigObject):
        try:
            self.tcp_data_package_service_pipe = Queue()
            print('start 213')
            self.TCPDataPackageService = multiprocessing.Process(target=TCPFlaskFunctions().startup,
                                                                 args=(
                                                                 FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP,
                                                                 FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort,
                                                                 self.tcp_data_package_service_pipe))
            print('starting now')
            self.TCPDataPackageService.start()
            self.pipeList['tcp_data_package_service_pipe'] = self.tcp_data_package_service_pipe
            self.FilterGroup.sources.append(self.tcp_data_package_service_pipe)
            time.sleep(2)
            return 1
        except Exception as e:
            logger.error(
                'there has been an exception in the individual starting of the Data Packages Service ' + str(e))
            return -1

    def stop_tcp_data_package_service(self):
        del self.pipeList['tcp_data_package_service_pipe']
        self.FilterGroup.sources.remove(self.tcp_data_package_service_pipe)
        try:
            self.TCPDataPackageService.terminate()
        except Exception as e:
            logger.error("there's been an exception in the termination of DataPackage Service " + str(e))
            return -1
        try:
            self.TCPDataPackageService.join()
        except Exception as e:
            logger.error("there's been an exception in the joining of DataPackage Service " + str(e))
            return -1
        self.tcp_data_package_service_pipe.close()
        return 1

    def start_ssl_data_package_service(self, FTSServiceStartupConfigObject):
        try:
            print('start 213')
            self.ssl_data_package_service = Queue()
            self.SSLDataPackageService = multiprocessing.Process(target=SSLFlaskFunctions().startup,
                                                                 args=(
                                                                 FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP,
                                                                 FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort,
                                                                 self.ssl_data_package_service))
            print('starting SSL now')
            self.SSLDataPackageService.start()
            self.pipeList['ssl_data_package_service'] = self.ssl_data_package_service
            self.FilterGroup.sources.append(self.ssl_data_package_service)
            time.sleep(2)
            return 1
        except Exception as e:
            logger.error(
                'there has been an exception in the individual starting of the Data Packages Service ' + str(e))
            return -1

    def stop_ssl_data_package_service(self):
        del (self.pipeList['ssl_data_package_service'])
        self.FilterGroup.sources.remove(self.ssl_data_package_service)
        try:
            self.SSLDataPackageService.terminate()
        except Exception as e:
            logger.error("there's been an exception in the termination of DataPackage Service " + str(e))
            return -1
        try:
            self.SSLDataPackageService.join()
        except Exception as e:
            logger.error("there's been an exception in the joining of DataPackage Service " + str(e))
            return -1
        self.ssl_data_package_service.close()
        return 1

    def start_SSL_CoT_service(self, FTSServiceStartupConfigObject):
        try:
            self.core_ssl_user_queue_send = Queue()
            self.service_ssl_user_queue_send = Queue()
            SSLCoTServicePipeFTS = Queue()
            SSLCoTServicePipeController = Queue()
            self.SSLCoTServicePipe = QueueManager(SSLCoTServicePipeFTS, SSLCoTServicePipeController)
            SSLCoTServicePipe = QueueManager(SSLCoTServicePipeController, SSLCoTServicePipeFTS)
            self.SSLCoTPoisonPill = multiprocessing.Event()
            self.SSLCoTPoisonPill.set()
            self.ReceiveConnectionsReset = multiprocessing.Event()
            self.SSLCoTService = multiprocessing.Process(target=SSLCoTServiceController().start, args=(
            FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceIP,
            FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServicePort, self.SSLCoTPoisonPill,
            self.service_ssl_user_queue_send, self.ReceiveConnectionsReset, SSLCoTServicePipe, self.core_ssl_user_queue_send))
            self.SSLCoTService.start()
            self.pipeList['SSLCoTServiceFTSPipe'] = self.SSLCoTServicePipe
            self.FilterGroup.sources.append(self.SSLCoTServicePipe)
            self.FilterGroup.receivers.append(self.SSLCoTServicePipe)
            print('SSL CoTService started')
            return 1
        except Exception as e:
            logger.error('an exception has been thrown in SSL CoT service startup ' + str(e))
            return -1

    def stop_SSL_CoT_service(self):
        try:
            self.SSLClientDataPipe.close()
            self.SSLCoTPoisonPill.clear()

            time.sleep(0.1)
            if self.SSLCoTService.is_alive():
                self.SSLCoTService.terminate()
                self.SSLCoTService.join()
            else:
                self.SSLCoTService.join()
            del (self.pipeList["SSLCoTServiceFTSPipe"])
            self.FilterGroup.sources.remove(self.SSLCoTServicePipe)
            self.FilterGroup.receivers.remove(self.SSLCoTServicePipe)

        except Exception as e:
            logger.error("there's been an exception in the stopping of CoT Service " + str(e))
            return -1
        return 1

    def start_federation_client_service(self, FTSServiceStartupConfigObject):
        FederationClientServicePipeFTS = Queue()
        FederationClientServicePipe = Queue()
        self.FederationClientServicePipeFTS = QueueManager(FederationClientServicePipeFTS, FederationClientServicePipe)
        FederationClientServicePipe = QueueManager(FederationClientServicePipe, FederationClientServicePipeFTS)
        self.FederationClientService = multiprocessing.Process(target=FederationClientServiceController().start,
                                                               args=(FederationClientServicePipe,))
        self.FederationClientService.start()
        self.pipeList['FederationClientServiceFTSPipe'] = self.FederationClientServicePipeFTS
        self.FilterGroup.sources.append(self.FederationClientServicePipeFTS)
        self.FilterGroup.receivers.append(self.FederationClientServicePipeFTS)
        return 1

    def stop_federation_client_service(self):
        try:
            del (self.pipeList['FederationClientServiceFTSPipe'])
            self.FilterGroup.receivers.remove(self.FederationClientServicePipeFTS)
            self.FilterGroup.sources.remove(self.FederationClientServicePipeFTS)
            if self.FederationClientService.is_alive():
                self.FederationClientService.terminate()
                self.FederationClientService.join()
            else:
                self.FederationClientService.join()

            self.FilterGroup.sources.remove(self.FederationClientServicePipeFTS)
            self.FilterGroup.receivers.remove(self.FederationClientServicePipeFTS)
            return 1
        except:
            return -1

    def start_federation_server_service(self, FTSServiceStartupConfigObject):
        try:
            ip = FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceIP
            port = FTSServiceStartupConfigObject.FederationServerService.FederationServerServicePort
            FederationServerServiceFTS = Queue()
            FederationServerServiceController = Queue()
            self.FederationServerServicePipeFTS = QueueManager(FederationServerServiceController,
                                                               FederationServerServiceFTS)
            FederationServerServicePipe = QueueManager(FederationServerServiceFTS, FederationServerServiceController)
            self.FederationServerService = multiprocessing.Process(
                target=FederationServerService().start, args=(FederationServerServicePipe, ip, port))
            self.FederationServerService.start()
            self.pipeList['FederationServerServiceFTSPipe'] = self.FederationServerServicePipeFTS
            self.FilterGroup.sources.append(self.FederationServerServicePipeFTS)
            self.FilterGroup.receivers.append(self.FederationServerServicePipeFTS)
            return 1
        except:
            return -1

    def stop_federation_server_service(self):
        try:
            if self.FederationServerService.is_alive():
                self.FederationServerService.terminate()
                self.FederationServerService.join()
            else:
                self.FederationServerService.join()
            self.FederationServerServicePipeFTS.close()
            self.FilterGroup.sources.remove(self.FederationServerServicePipeFTS)
            self.FilterGroup.receivers.remove(self.FederationServerServicePipeFTS)
            return 1
        except:
            return -1

    # change object name to FTSServiceStartupConfigObject
    def start_all(self, FTSServiceStartupConfigObject):
        import copy
        try:
            if FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus == 'start':
                self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus = FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus
                self.start_tcp_data_package_service(FTSServiceStartupConfigObject)
                if FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort != "":
                    self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort = FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort
                if FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP != "":
                    self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP = FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP

            elif FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus == 'stop':
                self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus = FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus
                self.stop_tcp_data_package_service()
            else:
                if FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP != self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP or self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort != FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort:
                    if FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus == "start" or self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus == "start":
                        self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP = FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP
                        self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort = FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort
                        self.stop_tcp_data_package_service()
                        self.start_tcp_data_package_service(FTSServiceStartupConfigObject)
                    else:
                        self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP = FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP

            if FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus == 'start':
                self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus = FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus
                self.start_ssl_data_package_service(FTSServiceStartupConfigObject)
                if FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort != "":
                    self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort = FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort
                if FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP != "":
                    self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP = FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP
            elif FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus == 'stop':
                self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus = FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus
                self.stop_ssl_data_package_service()
            else:
                if FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort != "":
                    self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort = FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort
                if FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP != self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP:
                    if FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus or self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus:
                        self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP = FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP
                        self.stop_ssl_data_package_service()
                        self.start_ssl_data_package_service(FTSServiceStartupConfigObject)
                    else:
                        self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP = FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP

            if FTSServiceStartupConfigObject.CoTService.CoTServiceStatus == 'start':
                self.FTSServiceStartupConfigObject.CoTService.CoTServiceStatus = FTSServiceStartupConfigObject.CoTService.CoTServiceStatus
                self.start_CoT_service(FTSServiceStartupConfigObject)
                if FTSServiceStartupConfigObject.CoTService.CoTServicePort != "":
                    self.FTSServiceStartupConfigObject.CoTService.CoTServicePort = FTSServiceStartupConfigObject.CoTService.CoTServicePort
                if FTSServiceStartupConfigObject.CoTService.CoTServiceIP != "":
                    self.FTSServiceStartupConfigObject.CoTService.CoTServiceIP = FTSServiceStartupConfigObject.CoTService.CoTServiceIP

            elif FTSServiceStartupConfigObject.CoTService.CoTServiceStatus == 'stop':
                self.FTSServiceStartupConfigObject.CoTService.CoTServiceStatus = FTSServiceStartupConfigObject.CoTService.CoTServiceStatus
                self.stop_CoT_service()
            else:
                pass

            if FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceStatus == 'start':
                self.FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceStatus = FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceStatus
                self.start_SSL_CoT_service(FTSServiceStartupConfigObject)
                if FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServicePort != "":
                    self.FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServicePort = FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServicePort
                if FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceIP != "":
                    self.FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceIP = FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceIP

            elif FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceStatus == 'stop':
                self.FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceStatus = FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceStatus
                self.stop_SSL_CoT_service()

            else:
                pass

            if FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceStatus == 'start':
                self.FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceStatus = FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceStatus
                self.start_federation_client_service(FTSServiceStartupConfigObject)
                if FTSServiceStartupConfigObject.FederationClientService.FederationClientServicePort != "":
                    self.FTSServiceStartupConfigObject.FederationClientService.FederationClientServicePort = FTSServiceStartupConfigObject.FederationClientService.FederationClientServicePort
                if FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceIP != "":
                    self.FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceIP = FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceIP


            elif FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceStatus == 'stop':
                self.FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceStatus = FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceStatus
                self.stop_federation_client_service()

            else:
                pass

            if FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus == 'start':
                self.FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus = FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus
                self.start_federation_server_service(FTSServiceStartupConfigObject)
                if FTSServiceStartupConfigObject.FederationServerService.FederationServerServicePort != "":
                    self.FTSServiceStartupConfigObject.FederationServerService.FederationServerServicePort = FTSServiceStartupConfigObject.FederationServerService.FederationServerServicePort
                if FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceIP != "":
                    self.FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceIP = FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceIP

            elif FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus == 'stop' \
                    and self.FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus != 'stop':
                self.FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus = FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus
                self.stop_federation_server_service()

            else:
                pass

            return 1
        except Exception as e:
            logger.error('there has been an exception in FTS start_all ' + str(e))
            return -1

    def restart_receive_connection_process(self):
        self.ReceiveConnectionsReset.set()
        return 1

    def receive_data_froCoT_service_thread(self, recv_pipe, clientArray, send_pipe):
        found = 0
        # pip data should be composed of 3 parts, [operation, modelObject, opensockets, connection_object(only necessary for add opp)]
        try:
            # TODO: change 'add' 'remove' 'update' and 'get' to an enumeration
            if not recv_pipe.empty():
                data = recv_pipe.get()
                self.socketCount = data[2]

                if data[0] == 'add':
                    # when add is called user is added to the user_dict with a connection object
                    if isinstance(data[1], Presence) and isinstance(data[3], Connection):
                        user_object = User(m_presence=data[1], connection=data[3])
                        self.user_dict[user_object.user_id] = user_object
                        self.RestAPIPipe.put(data[1])

                    else:
                        logger.error("error in adding client data to user_dict client presence data: " + str(data[1]) + " client connection data: " + str(data[3]))

                elif data[0] == 'remove':
                    self.user_dict[data[1].user_id].delete_connection(data[3])
                    if len(self.user_dict[data[1].user_id].connections) < 1:  # prevent users connected to more than one service being completely deleted upon disconnect
                        del self.user_dict[data[1].user_id]

                elif data[0] == 'update':
                    # when update is called user object is updated within the user_dict
                    if isinstance(data[1], Presence):
                        self.user_dict[data[1].modelObject.uid].m_presence = data[1]
                    else:
                        logger.error("error in updating existing client data in user_dict client presence data: " + str(data))

                elif data[0] == 'get':
                    if data[1] == None:
                        recv_pipe.put(self.user_dict)
                    else:
                        return_users = {}
                        for user_id, user_object in self.user_dict.items():
                            if user_object.get_connection(data[1]) is not None:
                                return_users[user_id] = user_object
                        send_pipe.put(return_users)

                return self.user_dict
            else:
                return self.user_dict

        except Exception as e:
            import traceback
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            logger.error("exception has been thrown in receive_data_froCoT_service_thread " + str(e) + " " + " error on line: "+str(line))
            return self.user_dict

    def receive_Rest_commands(self, kill):
        while kill.is_set() == False:
            try:
                command = self.RestAPICommandsFTS.get()
                if isinstance(command, tuple):
                    self.FederationClientServicePipeFTS.put(command)
                else:
                    function = getattr(self, command[0])
                    if len(command) >= 2:
                        output = function(command[1])
                    else:
                        output = function()
                    self.RestAPICommandsFTS.put(output)

            except Exception as e:
                logger.error('there has been an exception thrown in processing rest command ' + str(e))
                self.RestAPICommandsFTS.put('500')

    def check_server_status(self):
        return self.FTSServiceStartupConfigObject

    def help(self):
        print('start_all: to begin all services type')
        print('start_CoT_service: to begin CoT service type')
        print('start_data_package_service: to begin data package service  type')
        print('stop_all: to terminate all services type')
        print('stop_CoT_service: to terminate CoT service type')
        print('stop_data_package_service: to begin data package service type')
        print('check_service_status: to check the status of the services type')
        print('show_users: to show connected user information type')
        print('start_federation_client_service: to begin federation with another server')
        print('kill: to kill the full server type')

    def show_users(self):
        '''
        this method is used only by commands submitted over the rest interface
        '''
        data = [['', '', '']]
        objects = []
        output = []
        print(self.user_dict)
        for client in self.user_dict:
            data.append([client.IP, client.modelObject.detail.contact.callsign, client.modelObject.detail._group.name])
        for client in data:
            simpleClient = SimpleClient()
            simpleClient.callsign = client[1]
            simpleClient.team = client[2]
            simpleClient.ip = client[0]
            objects.append(simpleClient)

        output.append('total sockets: ' + str(self.socketCount))
        print(output)
        return objects

    def verify_output(self, input, example=None):
        try:
            if example == None:
                if input == None or input == -1:
                    return False
                else:
                    return True

            else:
                if isinstance(input, example):
                    return True
                else:
                    return False
        except Exception as e:
            logger.error('there has been an exception in FTS verifying output ' + str(e))
            return False

    def stop_all(self):
        try:
            DataPackageServiceOutput = self.stop_data_package_service()
            if self.verify_output(DataPackageServiceOutput):
                pass
            else:
                raise Exception('error stopping DataPackage Service')
            CoTServiceOutput = self.stop_CoT_service()
            if self.verify_output(CoTServiceOutput):
                pass
            else:
                raise Exception('error stopping CoT Service')
            return 1
        except Exception as e:
            logger.error('there has been an exception in FTS stop_all ' + str(e))
            return -1

    def kill(self):
        try:
            self.killSwitch = True
            return 1
        except Exception as e:
            logger.error('error in kill function ' + str(e))

    def checkPipes(self):
        try:
            for pipe in self.FilterGroup.sources:
                try:
                    data = AddDataToCoTList().recv(pipe, timeout=MainConfig.MainLoopDelay / 4000)
                except Exception as e:
                    logger.error('get pipe data failed ' + str(e))
                    continue
                # this runs in the event a new client has connected
                try:
                    if data == 0 or data is None:
                        continue
                    elif isinstance(data, list):
                        AddDataToCoTList().send(self.FilterGroup.receivers, data[0])
                        for client in self.user_dict.values():
                            AddDataToCoTList().send(self.FilterGroup.receivers, client.m_presence) # send presence objects of all clients too the service with a new client
                    # this runs in all other cases in which data is received
                    elif data != 0 and data is not None:
                        AddDataToCoTList().send(self.FilterGroup.receivers, data)
                    # this runs when a timeout is triggered
                    else:
                        pass
                except Exception as e:
                    logger.error('processing received connection data failed ' + str(e))
        except Exception as e:
            logger.error('exception in checking pipes ' + str(e))

    def startup(self, CoTPort, CoTIP, DataPackagePort, DataPackageIP, SSLDataPackagePort, SSLDataPackageIP, RestAPIPort,
                RestAPIIP, SSLCoTPort, SSLCoTIP, AutoStart, firstStart=False, UI="False"):
        try:
            self.dbController.remove_user()
            self.FTSServiceStartupConfigObject.RestAPIService.RestAPIServiceStatus = 'start'
            self.FTSServiceStartupConfigObject.RestAPIService.RestAPIServicePort = RestAPIPort
            self.FTSServiceStartupConfigObject.RestAPIServiceIP = RestAPIIP
            if firstStart:
                from datetime import datetime as dt
                self.StartupTime = dt.now()
            else:
                pass
            if AutoStart == 'False':
                StartupObject = FTSObj()
                StartupObject.RestAPIService.RestAPIServicePort = RestAPIPort
                StartupObject.RestAPIService.RestAPIServiceIP = RestAPIIP
                StartupObject.RestAPIService.RestAPIServiceStatus = 'start'
                self.start_restAPI_service(StartupObject)

            else:
                StartupObject = FTSObj()
                StartupObject.CoTService.CoTServiceIP = CoTIP
                StartupObject.CoTService.CoTServicePort = CoTPort
                StartupObject.CoTService.CoTServiceStatus = 'start'

                StartupObject.TCPDataPackageService.TCPDataPackageServiceIP = DataPackageIP
                StartupObject.TCPDataPackageService.TCPDataPackageServicePort = DataPackagePort
                StartupObject.TCPDataPackageService.TCPDataPackageServiceStatus = 'start'

                StartupObject.SSLDataPackageService.SSLDataPackageServiceIP = SSLDataPackageIP
                StartupObject.SSLDataPackageService.SSLDataPackageServicePort = SSLDataPackagePort
                StartupObject.SSLDataPackageService.SSLDataPackageServiceStatus = 'start'

                StartupObject.RestAPIService.RestAPIServicePort = RestAPIPort
                StartupObject.RestAPIService.RestAPIServiceIP = RestAPIIP
                StartupObject.RestAPIService.RestAPIServiceStatus = 'start'

                StartupObject.FederationClientService.FederationClientServiceStatus = 'start'

                # StartupObject.FederationServerService.FederationServerServiceStatus = ''

                StartupObject.SSLCoTService.SSLCoTServiceStatus = 'start'
                StartupObject.SSLCoTService.SSLCoTServiceIP = SSLCoTIP
                StartupObject.SSLCoTService.SSLCoTServicePort = SSLCoTPort
                self.start_restAPI_service(StartupObject)

                self.start_all(StartupObject)

            start_timer = time.time() - 60

            while True:
                time.sleep(MainConfig.MainLoopDelay / 1000)
                try:
                    if time.time() > start_timer+60:
                        start_timer = time.time()
                        logger.debug(str(self.user_dict))
                except Exception as e:
                    logger.error("the periodic debug message has thrown an error "+str(e))
                try:
                    self.checkPipes()
                except Exception as e:
                    logger.error("error in core FTS process Data Pipe " + str(e))
                try:
                    self.user_dict = self.receive_data_froCoT_service_thread(self.service_tcp_user_queue_send, self.user_dict, self.core_tcp_user_queue_send)
                except Exception as e:
                    logger.error("error thrown receiving clients from tcp CoT pipe " + str(e))
                try:
                    self.user_dict = self.receive_data_froCoT_service_thread(self.service_ssl_user_queue_send, self.user_dict, self.core_ssl_user_queue_send)
                except Exception as e:
                    logger.error("error thrown receiving clients from SSL CoT pipe " + str(e))
        except Exception as e:
            logger.error('exception in the startup of FTS ' + str(e))


import time


class QueueManager:
    def __init__(self, sender_queue: Queue, listener_queue: Queue):
        self.lock = multiprocessing.Event()
        self.lock.set()
        # queue too send data too
        self.sender_queue = sender_queue
        # queue too receive data from
        self.listener_queue = listener_queue

    def put(self, data):
        # print('putting data ' + str(data))
        try:
            self.sender_queue.put(data)
        except Exception as e:
            # print(e)
            pass
        # self.sender_queue.task_done()

    def get(self, timeout=None, **args):
        try:
            if timeout:
                gotten_data = self.listener_queue.get(timeout=timeout)
            else:
                gotten_data = self.listener_queue.get()
        except Exception as e:
            # print(e)
            return None
        return gotten_data

    def empty(self, timeout=None):
        empty = self.listener_queue.empty()
        return empty


class APIQueueManager:
    def __init__(self, sender_queue: Queue, listener_queue: Queue):
        self.lock = multiprocessing.Event()
        self.lock.set()
        # queue too send data too
        self.sender_queue = sender_queue
        # queue too receive data from
        self.listener_queue = listener_queue

    def put(self, data):
        if self.sender_queue.full():
            print('queue full')
        # print('putting data ' + str(data))
        try:
            self.sender_queue.put(data)
        except Exception as e:
            # print(e)
            pass
        # self.sender_queue.task_done()

    def get(self, **args):
        try:
            gotten_data = self.listener_queue.get()
        except Exception as e:
            # print(e)
            return None
        print('data gotten from queue ' + str(gotten_data))
        return gotten_data

    def empty(self, timeout=None):
        empty = self.listener_queue.empty()
        return empty


if __name__ == "__main__":
    """import importlib
    conf = importlib.import_module("FreeTAKServer-UI")
    FreeTAKServerUI = importlib.import_module("FreeTAKServer-UI.app", "run")
    y = FreeTAKServerUI.create_app()
    UIProc = multiprocessing.Process(target=FreeTAKServerUI.app, args=())
    UIProc.start()"""
    try:
        parser = argparse.ArgumentParser(description=OrchestratorConstants().FULLDESC)
        parser.add_argument('-CoTPort', type=int, help=OrchestratorConstants().COTPORTDESC,
                            default=FTSObj().CoTService.CoTServicePort)
        parser.add_argument('-CoTIP', type=str, help=OrchestratorConstants().COTIPDESC,
                            default=FTSObj().CoTService.CoTServiceIP)
        parser.add_argument('-SSLCoTPort', type=int, help=OrchestratorConstants().SSLCOTPORTDESC,
                            default=FTSObj().SSLCoTService.SSLCoTServicePort)
        parser.add_argument('-SSLCoTIP', type=str, help=OrchestratorConstants().SSLCOTIPDESC,
                            default=FTSObj().SSLCoTService.SSLCoTServiceIP)
        parser.add_argument('-DataPackagePort', type=int, help=OrchestratorConstants().APIPORTDESC,
                            default=FTSObj().TCPDataPackageService.TCPDataPackageServicePort)
        parser.add_argument('-DataPackageIP', type=str, help=OrchestratorConstants().APIPORTDESC,
                            default=FTSObj().TCPDataPackageService.TCPDataPackageServiceIP)
        parser.add_argument('-SSLDataPackagePort', type=int, help=OrchestratorConstants().APIPORTDESC,
                            default=FTSObj().SSLDataPackageService.SSLDataPackageServicePort)
        parser.add_argument('-SSLDataPackageIP', type=str, help=OrchestratorConstants().APIPORTDESC,
                            default=FTSObj().SSLDataPackageService.SSLDataPackageServiceIP)
        parser.add_argument('-RestAPIPort', type=int, help=OrchestratorConstants().APIPORTDESC,
                            default=FTSObj().RestAPIService.RestAPIServicePort)
        parser.add_argument('-RestAPIIP', type=str, help=OrchestratorConstants().APIPORTDESC,
                            default=FTSObj().RestAPIService.RestAPIServiceIP)
        parser.add_argument('-d', type=bool)
        parser.add_argument('-AutoStart', type=str,
                            help='whether or not you want all services to start or only the root service and the RestAPI service',
                            default='True')
        parser.add_argument('-UI', type=str, help="set to true if you would like to start UI on server startup")
        args = parser.parse_args()
        if MainConfig.first_start:
            ask_user_for_config()
        else:
            pass

        aotc = AtakOfTheCerts()
        aotc.generate_ca(expiry_time_secs=31536000)
        aotc.bake(common_name="server", cert="server", expiry_time_secs=31536000)
        aotc.bake(common_name="Client", cert="user", expiry_time_secs=31536000)
        import os

        if args.d:
            CreateStartupFilesController().create_daemon()
            os.system("systemd daemon-reload")
            os.system("systemctl start FreeTAKServer.service")
            exit(1)
        FTS().startup(args.CoTPort, args.CoTIP, args.DataPackagePort, args.DataPackageIP, args.SSLDataPackagePort,
                      args.SSLDataPackageIP, args.RestAPIPort, args.RestAPIIP, args.SSLCoTPort, args.SSLCoTIP,
                      args.AutoStart, True, args.UI)
    except Exception as e:
        print(e)

