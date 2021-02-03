import multiprocessing
import threading
import argparse
from FreeTAKServer.controllers.CreateStartupFilesController import CreateStartupFilesController
from FreeTAKServer.controllers.services.TCPDataPackageService import TCPDataPackageService as TCPFlaskFunctions
from FreeTAKServer.controllers.services.SSLDataPackageService import SSLDataPackageService as SSLFlaskFunctions
from FreeTAKServer.controllers.configuration.OrchestratorConstants import OrchestratorConstants
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.services.RestAPI import RestAPI
from FreeTAKServer.model.ServiceObjects.FTS import FTS as FTSObj
from FreeTAKServer.model.SimpleClient import SimpleClient
import time
from FreeTAKServer.controllers.AddDataToCoTList import AddDataToCoTList
from FreeTAKServer.model.FilterGroup import FilterGroup
from FreeTAKServer.controllers.services.SSLCoTServiceController import SSLCoTServiceController
from FreeTAKServer.controllers.services.TCPCoTServiceController import TCPCoTServiceController
from FreeTAKServer.controllers.services.federation.FederationClientService import FederationClientServiceController
from FreeTAKServer.controllers.services.federation.federation import FederationServerService
from FreeTAKServer.controllers.services.FederationServerServiceController import FederationServerServiceController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.controllers.certificate_generation import AtakOfTheCerts

loggingConstants = LoggingConstants()
logger = CreateLoggerController("FTS").getLogger()


# noinspection PyUnresolvedReferences
class FTS:

    def __init__(self):
        self.CoTService = None
        self.TCPDataPackageService = None
        self.UserCommand = None
        self.killSwitch = False
        self.ReceiveConnectionsReset = None
        self.CoTPoisonPill = None
        self.ClientDataPipe = None
        self.SSLClientDataPipe = None
        self.clientArray = []
        self.socketCount = 0
        self.pipeList = {}
        self.FilterGroup = FilterGroup()
        self.FTSServiceStartupConfigObject = FTSObj()
        self.dbController = DatabaseController()
        logger.propagate = True
        logger.info('something')

    def start_restAPI_service(self, StartupObjects):
        try:
            RestAPIPipe, self.RestAPIPipe = multiprocessing.Pipe(duplex=True)
            self.RestAPICommands, self.RestAPICommandsFTS = multiprocessing.Pipe()
            self.receive_Rest_stopper = threading.Event()
            self.receive_Rest_stopper.clear()
            self.receive_Rest = threading.Thread(target=self.receive_Rest_commands, args=(self.receive_Rest_stopper,))
            self.RestAPIProcess = multiprocessing.Process(target=RestAPI().startup, args=(RestAPIPipe, self.RestAPICommands, StartupObjects.RestAPIService.RestAPIServiceIP, StartupObjects.RestAPIService.RestAPIServicePort, self.StartupTime))
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
            self.ClientDataPipe, ClientDataPipeParentChild = multiprocessing.Pipe()
            self.TCPCoTService, self.TCPCoTServiceFTSPipe = multiprocessing.Pipe(duplex=True)
            self.CoTPoisonPill = multiprocessing.Event()
            self.CoTPoisonPill.set()
            self.ReceiveConnectionsReset = multiprocessing.Event()
            self.CoTService = multiprocessing.Process(target=TCPCoTServiceController().start, args=(FTSServiceStartupConfigObject.CoTService.CoTServiceIP, FTSServiceStartupConfigObject.CoTService.CoTServicePort, self.CoTPoisonPill, ClientDataPipeParentChild, self.ReceiveConnectionsReset, self.TCPCoTService))
            self.CoTService.start()
            self.pipeList['TCPCoTServiceFTSPipe'] = self.TCPCoTServiceFTSPipe
            self.FilterGroup.receivers.append(self.TCPCoTServiceFTSPipe)
            self.FilterGroup.sources.append(self.TCPCoTServiceFTSPipe)
            print('CoTService started')
            return 1
        except Exception as e:
            logger.error('an exception has been thrown in CoT service startup ' + str(e))
            return -1

    def stop_CoT_service(self):
        try:
            self.ClientDataPipe.close()
            self.CoTPoisonPill.clear()

            time.sleep(1)
            if self.CoTService.is_alive():
                self.CoTService.terminate()
                self.CoTService.join()
            else:
                self.CoTService.join()

            self.FilterGroup.sources.remove(self.TCPCoTServiceFTSPipe)
            self.FilterGroup.receivers.remove(self.TCPCoTServiceFTSPipe)

        except Exception as e:
            logger.error("there's been an exception in the stopping of CoT Service " + str(e))
            return -1
        return 1

    def start_tcp_data_package_service(self, FTSServiceStartupConfigObject):
        try:
            tcp_data_package_service_pipe, self.tcp_data_package_service_pipe = multiprocessing.Pipe(duplex=True)
            print('start 213')
            self.TCPDataPackageService = multiprocessing.Process(target=TCPFlaskFunctions().startup,
                                                                 args=(FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP, FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort, tcp_data_package_service_pipe))
            print('starting now')
            self.TCPDataPackageService.start()
            self.pipeList['tcp_data_package_service_pipe'] = self.tcp_data_package_service_pipe
            self.FilterGroup.sources.append(self.tcp_data_package_service_pipe)
            time.sleep(2)
            return 1
        except Exception as e:
            logger.error('there has been an exception in the individual starting of the Data Packages Service ' + str(e))
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
            ssl_data_package_service, self.ssl_data_package_service = multiprocessing.Pipe(duplex=True)
            self.SSLDataPackageService = multiprocessing.Process(target=SSLFlaskFunctions().startup,
                                                                 args=(FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP, FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort, ssl_data_package_service))
            print('starting SSL now')
            self.SSLDataPackageService.start()
            self.pipeList['ssl_data_package_service'] = self.ssl_data_package_service
            self.FilterGroup.sources.append(self.ssl_data_package_service)
            time.sleep(2)
            return 1
        except Exception as e:
            logger.error('there has been an exception in the individual starting of the Data Packages Service ' + str(e))
            return -1

    def stop_ssl_data_package_service(self):
        del(self.pipeList['ssl_data_package_service'])
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
            self.SSLClientDataPipe, SSLClientDataPipeParentChild = multiprocessing.Pipe()
            self.SSLCoTServicePipe, self.SSLCoTServiceFTSPipe = multiprocessing.Pipe()
            self.SSLCoTPoisonPill = multiprocessing.Event()
            self.SSLCoTPoisonPill.set()
            self.ReceiveConnectionsReset = multiprocessing.Event()
            self.SSLCoTService = multiprocessing.Process(target=SSLCoTServiceController().start, args=(FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceIP, FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServicePort, self.SSLCoTPoisonPill, SSLClientDataPipeParentChild, self.ReceiveConnectionsReset, self.SSLCoTServicePipe))
            self.SSLCoTService.start()
            self.pipeList['SSLCoTServiceFTSPipe'] = self.SSLCoTServiceFTSPipe
            self.FilterGroup.sources.append(self.SSLCoTServiceFTSPipe)
            self.FilterGroup.receivers.append(self.SSLCoTServiceFTSPipe)
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
            del(self.pipeList["SSLCoTServiceFTSPipe"])
            self.FilterGroup.sources.remove(self.SSLCoTServicePipe)
            self.FilterGroup.receivers.remove(self.SSLCoTServicePipe)

        except Exception as e:
            logger.error("there's been an exception in the stopping of CoT Service " + str(e))
            return -1
        return 1

    def start_federation_client_service(self, FTSServiceStartupConfigObject):
        FederationClientServicePipe, self.FederationClientServicePipeFTS = multiprocessing.Pipe(True)
        self.FederationClientService = multiprocessing.Process(target=FederationClientServiceController().start, args=(FederationClientServicePipe,))
        self.FederationClientService.start()
        self.pipeList['FederationClientServiceFTSPipe'] = self.FederationClientServicePipeFTS
        self.FilterGroup.sources.append(self.FederationClientServicePipeFTS)
        self.FilterGroup.receivers.append(self.FederationClientServicePipeFTS)
        return 1

    def stop_federation_client_service(self):
        try:
            del(self.pipeList['FederationClientServiceFTSPipe'])
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
        except BaseException:
            return -1

    def start_federation_server_service(self, FTSServiceStartupConfigObject):
        try:
            ip = FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceIP
            port = FTSServiceStartupConfigObject.FederationServerService.FederationServerServicePort
            FederationServerServicePipe, self.FederationServerServicePipeFTS = multiprocessing.Pipe()
            self.FederationServerService = multiprocessing.Process(
                target=FederationServerService().start, args=(FederationServerServicePipe, ip, port))
            self.FederationServerService.start()
            self.pipeList['FederationServerServiceFTSPipe'] = self.FederationServerServicePipeFTS
            self.FilterGroup.sources.append(self.FederationServerServicePipeFTS)
            self.FilterGroup.receivers.append(self.FederationServerServicePipeFTS)
            return 1
        except BaseException:
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
        except BaseException:
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
                if FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort != "":
                    self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort = FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort
                if FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP != self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP:
                    if FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus or self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus:
                        self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP = FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP
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

    def receive_data_froCoT_service_thread(self, pipe, clientArray):
        found = 0
        try:
            if pipe.poll(timeout=0.01):
                data = pipe.recv()
                self.socketCount = data[2]
                if data[0] == 'add':
                    clientArray.append(data[1])
                    self.RestAPIPipe.send(data[1])
                else:
                    for client in clientArray:
                        if client.ID == data[1].ID:
                            clientArray.remove(client)
                            found = 1
                        else:
                            pass
                    if found == 0:
                        for client in clientArray:
                            if client.IP == data[1].IP and client.modelObject.detail.contact.callsign == data[1].modelObject.detail.contact.callsign:
                                clientArray.remove(client)
                                found = 1
                            else:
                                pass
                    else:
                        pass

                return self.clientArray
            else:
                return self.clientArray
        except Exception as e:
            return self.clientArray

    def receive_Rest_commands(self, kill):
        while kill.is_set() == False:
            try:
                command = self.RestAPICommandsFTS.recv()
                if isinstance(command, tuple):
                    self.FederationClientServicePipeFTS.send(command)
                else:
                    function = getattr(self, command[0])
                    if len(command) >= 2:
                        output = function(command[1])
                    else:
                        output = function()
                    self.RestAPICommandsFTS.send(output)

            except Exception as e:
                logger.error('there has been an exception thrown in processing rest command ' + str(e))
                self.RestAPICommandsFTS.send('500')

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
        print(self.clientArray)
        for client in self.clientArray:
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
            if example is None:
                if input is None or input == -1:
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
                    data = AddDataToCoTList().recv(pipe)
                except Exception as e:
                    logger.error('get pipe data failed ' + str(e))
                    continue
                # this runs in the event a new client has connected
                try:
                    if isinstance(data, list):
                        AddDataToCoTList().send(self.FilterGroup.receivers, data[0])
                        for client in self.clientArray:
                            AddDataToCoTList().send(self.FilterGroup.receivers, client)
                    # this runs in all other cases in which data is received
                    elif data != 0 and data is not None:
                        try:
                            print('data received in FTS ' + str(data.xmlString))
                        except BaseException:
                            pass
                        AddDataToCoTList().send(self.FilterGroup.receivers, data)
                    # this runs when a timeout is triggered
                    else:
                        pass
                except Exception as e:
                    logger.error('processing received connection data failed ' + str(e))
        except Exception as e:
            pass

    def startup(self, CoTPort, CoTIP, DataPackagePort, DataPackageIP, SSLDataPackagePort, SSLDataPackageIP, RestAPIPort, RestAPIIP, SSLCoTPort, SSLCoTIP, AutoStart, firstStart=False, UI="False"):
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

                #StartupObject.FederationServerService.FederationServerServiceStatus = ''

                StartupObject.SSLCoTService.SSLCoTServiceStatus = 'start'
                StartupObject.SSLCoTService.SSLCoTServiceIP = SSLCoTIP
                StartupObject.SSLCoTService.SSLCoTServicePort = SSLCoTPort
                self.start_restAPI_service(StartupObject)

                self.start_all(StartupObject)

            while True:
                try:
                    self.checkPipes()
                except Exception as e:
                    logger.error("error in core FTS process Data Pipe " + str(e))
                try:
                    self.clientArray = self.receive_data_froCoT_service_thread(self.ClientDataPipe, self.clientArray)
                except Exception as e:
                    logger.error("error thrown receiving clients from tcp CoT pipe " + str(e))
                try:
                    self.clientArray = self.receive_data_froCoT_service_thread(self.SSLClientDataPipe, self.clientArray)
                except Exception as e:
                    logger.error("error thrown receiving clients from SSL CoT pipe " + str(e))
        except Exception as e:
            logger.error('exception in the startup of FTS ' + str(e))


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
        parser.add_argument('-AutoStart', type=str, help='whether or not you want all services to start or only the root service and the RestAPI service', default='True')
        parser.add_argument('-UI', type=str, help="set to true if you would like to start UI on server startup")
        args = parser.parse_args()
        AtakOfTheCerts().bake_startup()
        CreateStartupFilesController()
        FTS().startup(args.CoTPort, args.CoTIP, args.DataPackagePort, args.DataPackageIP, args.SSLDataPackagePort, args.SSLDataPackageIP, args.RestAPIPort, args.RestAPIIP, args.SSLCoTPort, args.SSLCoTIP, args.AutoStart, True, args.UI)
    except Exception as e:
        print(e)
