import multiprocessing
import threading
import argparse
from flask_cors import CORS
from FreeTAKServer.controllers.CreateStartupFilesController import CreateStartupFilesController
from FreeTAKServer.controllers.Orchestrator import Orchestrator
from FreeTAKServer.controllers.DataPackageServer import FlaskFunctions
from FreeTAKServer.controllers.configuration.OrchestratorConstants import OrchestratorConstants
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.AsciiController import AsciiController
from FreeTAKServer.controllers.RestAPI import RestAPI
from FreeTAKServer.controllers.model.FTS import FTS as FTSObj
from FreeTAKServer.controllers.model.SimpleClient import SimpleClient
from FreeTAKServer.controllers.configuration.ArgumentConstants import ArgumentConstants
import time
from queue import Queue
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
        self.clientInformationArray = []
        self.FTSServiceStartupConfigObject = FTSObj()
        logger.propagate = True
        logger.info('something')

    def start_restAPI_service(self, StartupObjects):
        try:
            self.RestAPIPipe, self.RestAPIOrchestratorPipe = multiprocessing.Pipe()
            self.RestAPICommands, self.RestAPICommandsFTS = multiprocessing.Pipe()
            self.RestAPIUpdates, self.RestAPIUpdatesFTS = multiprocessing.Pipe()
            self.receive_Rest_stopper = threading.Event()
            self.receive_Rest_stopper.clear()
            self.receive_Rest = threading.Thread(target=self.receive_Rest_commands, args=(self.receive_Rest_stopper,))
            self.RestAPIProcess = multiprocessing.Process(target=RestAPI().startup, args=(self.RestAPIPipe, self.RestAPICommands, self.RestAPIUpdates, StartupObjects.RestAPIService.RestAPIServiceIP, StartupObjects.RestAPIService.RestAPIServicePort))
            self.receive_Rest.start()
            self.RestAPIProcess.start()
            users = self.show_users()
            self.RestAPIUpdatesFTS.send(users)
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
            threading.Thread(target=self.receive_data_froCoT_service_thread, daemon=True).start()
            self.CoTPoisonPill = multiprocessing.Event()
            self.CoTPoisonPill.set()
            self.ReceiveConnectionsReset = multiprocessing.Event()
            self.CoTService = multiprocessing.Process(target=Orchestrator().start, args=(FTSServiceStartupConfigObject.CoTService.CoTServiceIP, FTSServiceStartupConfigObject.CoTService.CoTServicePort, self.CoTPoisonPill, ClientDataPipeParentChild, self.ReceiveConnectionsReset, self.RestAPIOrchestratorPipe))
            self.CoTService.start()
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
            logger.error('there has been an exception in the individual starting of the Data Packages Service')
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

    def receive_data_froCoT_service_thread(self):
        while True:
            found = 0
            try:
                data = self.ClientDataPipe.recv()
                print(data)
                self.socketCount = data[2]
                self.clientInformationArray = data[3]
                if data[0] == 'add':
                    self.clientArray.append(data[1])
                else:
                    for client in self.clientArray:
                        if client.ID == data[1].ID:
                            self.clientArray.remove(client)
                            found = 1
                        else:
                            pass
                    if found == 0:
                        for client in self.clientArray:
                            if client.IP == data[1].IP and client.modelObject.detail.contact.callsign == data[1].modelObject.detail.contact.callsign:
                                self.clientArray.remove(client)
                                found = 1
                            else:
                                pass
                    else:
                        pass
                userData = self.show_users()
                self.RestAPIUpdatesFTS.send(userData)
            except Exception as e:
                pass

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

    def help(self):
        print('start_all: to begin all services type')
        print('start_CoT_service: to begin CoT service type')
        print('start_data_package_service: to begin data package service  type')
        print('stop_all: to terminate all services type')
        print('stop_CoT_service: to terminate CoT service type')
        print('stop_data_package_service: to begin data package service type')
        print('check_service_status: to check the status of the services type')
        print('show_users: to show connected user information type')
        print('kill: to kill the full server type')

    def check_service_status(self):
        print('Data Package Service : ' + str(self.DataPackageService.is_alive()))
        print('CoT service is_alive : ' + str(self.CoTService.is_alive()))
        return 1

    def show_client_array(self):
        print(self.clientInformationArray)
        print('length is ' + len(self.clientInformationArray))
        return 1

    def show_users(self):
        data = [['', '', '']]
        objects = []
        output = []
        print(self.clientArray)
        for client in self.clientArray:
            data.append([client.modelObject.detail.contact.callsign, client.modelObject.detail.get__group().name, client.IP[0]])
        #col_width = max(len(word) for row in data for word in row) + 2  # padding
        #for row in data:
        #    print("".join(word.ljust(col_width) for word in row))
        #    output.append("".join(word.ljust(col_width) for word in row))
        for client in data:
            simpleClient = SimpleClient()
            simpleClient.callsign = client[0]
            simpleClient.team = client[1]
            simpleClient.ip = client[2]
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

    def empty(self):
        return 1

    def receive_input(self):
        AsciiController().ascii()
        while self.killSwitch == False:
            try:
                self.UserCommand = str(input('FTS$ ')) or 'empty'
                try:
                    function = getattr(self, self.UserCommand)
                except:
                    logger.error('this is not a valid command')
                functionOutput = function()
                if self.verify_output(functionOutput):
                    pass
                else:
                    raise Exception('function returned bad data')
            except Exception as e:
                logger.error('error in processing your request ' + str(e))
        self.stop_all()
    
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
                time.sleep(1000)
        except Exception as e:
            logger.error('exception in the startup of FTS ' + str(e))

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=OrchestratorConstants().FULLDESC)
        parser.add_argument('-CoTPort', type=int, help=OrchestratorConstants().COTPORTDESC,
                            default=FTSObj().CoTService.CoTServicePort)
        parser.add_argument('-CoTIP', type=str, help=OrchestratorConstants().CoTIP,
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