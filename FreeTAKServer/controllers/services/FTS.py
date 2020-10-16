import multiprocessing
import threading
import argparse
from FreeTAKServer.controllers.CreateStartupFilesController import CreateStartupFilesController
from FreeTAKServer.controllers.services.DataPackageServer import FlaskFunctions
from FreeTAKServer.controllers.configuration.OrchestratorConstants import OrchestratorConstants
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.services.RestAPI import RestAPI
from FreeTAKServer.model.ServiceObjects.FTS import FTS as FTSObj
from FreeTAKServer.model.SimpleClient import SimpleClient
import time
from FreeTAKServer.controllers.AddDataToCoTList import AddDataToCoTList
from FreeTAKServer.model.FilterGroup import FilterGroup
from FreeTAKServer.controllers.services.TCPCoTServiceController import TCPCoTServiceController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController

loggingConstants = LoggingConstants()
logger = CreateLoggerController("FTS").getLogger()


class FTS:

    def __init__(self):
        self.CoTService = None
        self.DataPackageService = None
        self.UserCommand = None
        self.killSwitch = False
        self.ReceiveConnectionsReset = None
        self.CoTPoisonPill = None
        self.ClientDataPipe = None
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
            self.RestAPIProcess = multiprocessing.Process(target=RestAPI().startup, args=(RestAPIPipe, self.RestAPICommands, StartupObjects.RestAPIService.RestAPIServiceIP, StartupObjects.RestAPIService.RestAPIServicePort))
            self.receive_Rest.start()
            self.RestAPIProcess.start()
            self.pipeList['restAPI'] = self.RestAPIPipe
            self.FilterGroup.sources.append(self.RestAPIPipe)
            return 1
        except Exception as e:
            logger.error('There has been an exception thrown in the startup of the restAPI service '+str(e))
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

            time.sleep(0.1)
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

    def start_data_package_service(self, FTSServiceStartupConfigObject):
        try:
            print('start 213')
            self.DataPackageService = multiprocessing.Process(target=FlaskFunctions().startup,
                                                              args=(FTSServiceStartupConfigObject.DataPackageService.DataPackageServiceIP, FTSServiceStartupConfigObject.DataPackageService.DataPackageServicePort))
            print('starting now')
            self.DataPackageService.start()
            time.sleep(2)
            return 1
        except Exception as e:
            logger.error('there has been an exception in the individual starting of the Data Packages Service ' + str(e))
            return -1

    def stop_data_package_service(self):
        try:
            self.DataPackageService.terminate()
        except Exception as e:
            logger.error("there's been an exception in the termination of DataPackage Service " + str(e))
            return -1
        try:
            self.DataPackageService.join()
        except Exception as e:
            logger.error("there's been an exception in the joining of DataPackage Service " + str(e))
            return -1
        return 1

    #change object name to FTSServiceStartupConfigObject
    def start_all(self, FTSServiceStartupConfigObject):
        try:
            self.FTSServiceStartupConfigObject = FTSServiceStartupConfigObject
            if FTSServiceStartupConfigObject.DataPackageService.DataPackageServiceStatus == 'start':
                self.start_data_package_service(FTSServiceStartupConfigObject)

            elif FTSServiceStartupConfigObject.DataPackageService.DataPackageServiceStatus == 'stop':
                self.stop_data_package_service()
            else:
                pass

            if FTSServiceStartupConfigObject.CoTService.CoTServiceStatus == 'start':
                self.start_CoT_service(FTSServiceStartupConfigObject)

            elif FTSServiceStartupConfigObject.CoTService.CoTServiceStatus == 'stop':
                self.stop_CoT_service()
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
                userData = self.show_users()
                self.RestAPIPipe.send(userData)
                return self.clientArray
            else:
                return self.clientArray
        except Exception as e:
            return self.clientArray

    def receive_Rest_commands(self, kill):
        while kill.is_set() == False:
            try:
                command = self.RestAPICommandsFTS.recv()
                function = getattr(self, command[0])
                if len(command)>=2:
                    output = function(command[1])
                else:
                    output = function()
                self.RestAPICommandsFTS.send(output)

            except Exception as e:
                logger.error('there has been an exception thrown in processing rest command ' + str(e))
                self.RestAPICommandsFTS.send('500')

            except Exception as e:
                logger.error('there has been a critical exception ' + str(e))
                break

    def check_server_status(self):
        return self.FTSServiceStartupConfigObject

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

        output.append('total sockets: '+str(self.socketCount))
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
            logger.error('error in kill function '+str(e))

    def checkPipes(self):
        try:
            for pipe in self.FilterGroup.sources:
                data = AddDataToCoTList().recv(pipe)
                #this runs in the event a new client has connected
                if isinstance(data, list):
                    AddDataToCoTList().send(self.FilterGroup.receivers, data[0])
                    for client in self.clientArray:
                        AddDataToCoTList().send(self.FilterGroup.receivers, client)
                # this runs in all other cases in which data is received
                elif data != 0:
                    try:
                        print('data received in FTS ' + str(data.xmlString))
                    except:
                        pass
                    AddDataToCoTList().send(self.FilterGroup.receivers, data)
                # this runs when a timeout is triggered
                else:
                    pass
        except Exception as e:
            pass
    
    def startup(self, CoTPort, CoTIP, DataPackagePort, DataPackageIP, RestAPIPort, RestAPIIP, AutoStart):
        try:
            if AutoStart == 'False':
                StartupObject = FTSObj()
                StartupObject.RestAPIService.RestAPIServicePort = RestAPIPort
                StartupObject.RestAPIService.RestAPIServiceIP = RestAPIIP
                self.start_restAPI_service(StartupObject)

            else:
                StartupObject = FTSObj()
                StartupObject.CoTService.CoTServiceIP = CoTIP
                StartupObject.CoTService.CoTServicePort = CoTPort
                StartupObject.CoTService.CoTServiceStatus = 'start'

                StartupObject.DataPackageService.DataPackageServiceIP = DataPackageIP
                StartupObject.DataPackageService.DataPackageServicePort = DataPackagePort
                StartupObject.DataPackageService.DataPackageServiceStatus = 'start'

                StartupObject.RestAPIService.RestAPIServicePort = RestAPIPort
                StartupObject.RestAPIService.RestAPIServiceIP = RestAPIIP
                StartupObject.RestAPIService.RestAPIServiceStatus = 'start'

                self.start_restAPI_service(StartupObject)

                self.start_all(StartupObject)


            while True:
                self.checkPipes()
                self.clientArray = self.receive_data_froCoT_service_thread(self.ClientDataPipe, self.clientArray)

        except Exception as e:
            logger.error('exception in the startup of FTS ' + str(e))

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=OrchestratorConstants().FULLDESC)
        parser.add_argument('-CoTPort', type=int, help=OrchestratorConstants().COTPORTDESC,
                            default=FTSObj().CoTService.CoTServicePort)
        parser.add_argument('-CoTIP', type=str, help=OrchestratorConstants().COTIPDESC,
                            default=FTSObj().CoTService.CoTServiceIP)
        parser.add_argument('-DataPackagePort', type=int, help=OrchestratorConstants().APIPORTDESC,
                            default=FTSObj().DataPackageService.DataPackageServicePort)
        parser.add_argument('-DataPackageIP', type=str, help=OrchestratorConstants().APIPORTDESC,
                            default=FTSObj().DataPackageService.DataPackageServiceIP)
        parser.add_argument('-RestAPIPort', type=int, help=OrchestratorConstants().APIPORTDESC,
                            default=FTSObj().RestAPIService.RestAPIServicePort)
        parser.add_argument('-RestAPIIP', type=str, help=OrchestratorConstants().APIPORTDESC,
                            default=FTSObj().RestAPIService.RestAPIServiceIP)
        parser.add_argument('-AutoStart', type=str, help='wether or not you want all services to start or only the root service and the RestAPI service', default='True')
        args = parser.parse_args()
        CreateStartupFilesController()
        FTS().startup(args.CoTPort, args.CoTIP, args.DataPackagePort, args.DataPackageIP, args.RestAPIPort, args.RestAPIIP, args.AutoStart)
    except Exception as e:
        print(e)