import argparse
import linecache
import multiprocessing
import pathlib
import random
import sys
import threading

from digitalpy.config.impl.inifile_configuration import InifileConfiguration
from digitalpy.config.configuration import Configuration
from digitalpy.core.impl.default_factory import DefaultFactory
from digitalpy.core.object_factory import ObjectFactory
from digitalpy.registration.registration_handler import RegistrationHandler
from digitalpy.routing.routing_proxy import RoutingProxy

from FreeTAKServer.controllers.CreateStartupFilesController import (
    CreateStartupFilesController,
)

CreateStartupFilesController()

import queue
import time
from multiprocessing import Queue

from FreeTAKServer.controllers.AddDataToCoTList import AddDataToCoTList
from FreeTAKServer.controllers.util.certificate_generation import AtakOfTheCerts
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from FreeTAKServer.controllers.configuration.OrchestratorConstants import (
    OrchestratorConstants,
)
from FreeTAKServer.controllers.configuration.configuration_wizard import ask_user_for_config
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import (
    DatabaseController,
)
from FreeTAKServer.controllers.services.federation.federation import (
    FederationServerService,
)
from FreeTAKServer.controllers.services.federation.FederationClientService import (
    FederationClientServiceController,
)
from FreeTAKServer.controllers.services.RestAPI import RestAPI
from FreeTAKServer.controllers.services.SSLCoTServiceController import (
    SSLCoTServiceController,
)
from FreeTAKServer.controllers.services.SSLDataPackageService import (
    SSLDataPackageService as SSLFlaskFunctions,
)
from FreeTAKServer.controllers.connection.TCPCoTServiceController import (
    TCPCoTServiceController,
)
from FreeTAKServer.controllers.services.TCPDataPackageService import (
    TCPDataPackageService as TCPFlaskFunctions,
)
from FreeTAKServer.model.Connection import Connection
from FreeTAKServer.model.Enumerations.connectionTypes import ConnectionTypes
from FreeTAKServer.model.Enumerations.serviceTypes import ServiceTypes
from FreeTAKServer.model.FilterGroup import FilterGroup
from FreeTAKServer.model.ServiceObjects.FTS import FTS as FTSObj
from FreeTAKServer.model.SimpleClient import SimpleClient
from FreeTAKServer.model.SpecificCoT.Presence import Presence
from FreeTAKServer.model.User import User

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

loggingConstants = LoggingConstants(log_name="FTS_FTSCore")
logger = CreateLoggerController(
    "FTS_FTSCore", logging_constants=loggingConstants
).getLogger()

loggingConstants = LoggingConstants()


# noinspection PyUnresolvedReferences
class FTS:
    def __init__(self):
        self.data_from_services = 0
        self.FederationClientService = None
        self.FederationServerService = None
        self.SSLCoTService = None
        self.SSLDataPackageService = None
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

        # the central digitalpy configuration used throughout the application
        self.configuration: Configuration = None

    def start_rest_api_service(self, StartupObjects):
        """this method starts the rest api service and instantiates ISC protocols

        :param StartupObjects:
        :return:
        """
        try:
            self.RestAPIPipe = Queue()
            restapicommandsthread = Queue()
            restapicommandsmain = Queue()
            self.RestAPICommandsFTS = QueueManager(
                restapicommandsmain, restapicommandsthread
            )
            RestAPICommandsFTS = QueueManager(
                restapicommandsthread, restapicommandsmain
            )
            self.receive_Rest_stopper = multiprocessing.Event()
            self.receive_Rest_stopper.clear()
            self.receive_Rest = threading.Thread(
                target=self.receive_Rest_commands, args=(self.receive_Rest_stopper,)
            )
            self.RestAPIProcess = multiprocessing.Process(
                target=RestAPI().startup,
                args=(
                    self.RestAPIPipe,
                    RestAPICommandsFTS,
                    StartupObjects.RestAPIService.RestAPIServiceIP,
                    StartupObjects.RestAPIService.RestAPIServicePort,
                    self.StartupTime,
                ),
            )
            self.receive_Rest.start()
            self.RestAPIProcess.start()
            self.pipeList["restAPI"] = self.RestAPIPipe
            self.FilterGroup.add_source(self.RestAPIPipe, ServiceTypes.APISERVICE)
            return 1
        except Exception as e:
            logger.error(
                "There has been an exception thrown in the startup of the restAPI service "
                + str(e)
            )
            return -1

    def stop_rest_api_service(self):
        """this method terminates the REST API process and closses
        associated resources

        :return:
        """
        try:
            self.RestAPIProcess.terminate()
            self.RestAPIProcess.join()
            self.receive_Rest_stopper.set()
            self.receive_Rest.join()
        except Exception as e:
            logger.error("an exception has been thrown in RestAPI Startup " + str(e))

    def start_cot_service(self, FTSServiceStartupConfigObject):
        """this method starts the cot service process and the required ISC resources

        :param FTSServiceStartupConfigObject: object containing service startup and configuration information
        :return:
        """
        try:
            self.core_tcp_user_queue_send = Queue()
            self.service_tcp_user_queue_send = Queue()
            TCPCoTServiceThread = Queue()
            TCPCoTServiceFTS = Queue()
            self.TCPCoTService = QueueManager(TCPCoTServiceThread, TCPCoTServiceFTS)
            TCPCoTService = QueueManager(TCPCoTServiceFTS, TCPCoTServiceThread)
            print("event event about to be created")
            self.CoTPoisonPill = multiprocessing.Event()
            self.CoTPoisonPill.set()
            self.ReceiveConnectionsReset = multiprocessing.Event()
            self.CoTService = multiprocessing.Process(
                target=TCPCoTServiceController().start,
                args=(
                    FTSServiceStartupConfigObject.CoTService.CoTServiceIP,
                    FTSServiceStartupConfigObject.CoTService.CoTServicePort,
                    self.CoTPoisonPill,
                    self.service_tcp_user_queue_send,
                    self.ReceiveConnectionsReset,
                    TCPCoTService,
                    self.core_tcp_user_queue_send,
                    ObjectFactory.get_instance("factory"),
                ),
            )
            self.CoTService.start()
            self.pipeList["TCPCoTServiceFTSPipe"] = self.TCPCoTService
            self.FilterGroup.add_receiver(
                self.TCPCoTService, ServiceTypes.TCPCOTSERVICE
            )
            self.FilterGroup.add_source(self.TCPCoTService, ServiceTypes.TCPCOTSERVICE)
            print("CoTService started")
            return 1
        except Exception as e:
            logger.error(
                "an exception has been thrown in CoT service startup " + str(e)
            )
            return -1

    def stop_cot_service(self):
        """terminate the cot service process and associated ISC resources

        :return:
        """
        try:
            # self.ClientDataPipe.close()
            self.CoTPoisonPill.clear()

            time.sleep(1)
            if self.CoTService.is_alive():
                self.CoTService.terminate()
                self.CoTService.join()
            else:
                self.CoTService.join()

            self.FilterGroup.remove_source(ServiceTypes.TCPCOTSERVICE)
            self.FilterGroup.remove_receiver(ServiceTypes.TCPCOTSERVICE)

        except Exception as e:
            logger.error(
                "there's been an exception in the stopping of CoT Service " + str(e)
            )
            return -1
        return 1

    def start_tcp_data_package_service(self, FTSServiceStartupConfigObject):
        """initiate TCP DP service and ISC resources

        :param FTSServiceStartupConfigObject:
        :return:
        """
        try:
            self.tcp_data_package_service_pipe = Queue()
            print("start 213")
            self.TCPDataPackageService = multiprocessing.Process(
                target=TCPFlaskFunctions().startup,
                args=(
                    FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP,
                    FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort,
                    self.tcp_data_package_service_pipe,
                ),
            )
            print("starting now")
            self.TCPDataPackageService.start()
            self.pipeList[
                "tcp_data_package_service_pipe"
            ] = self.tcp_data_package_service_pipe
            self.FilterGroup.add_source(
                self.tcp_data_package_service_pipe, ServiceTypes.TCPDPSERVICE
            )
            time.sleep(2)
            return 1
        except Exception as e:
            logger.error(
                "there has been an exception in the individual starting of the Data Packages Service "
                + str(e)
            )
            return -1

    def stop_tcp_data_package_service(self):
        """stop TCP DP service and terminate ISC resources

        :return:
        """
        del self.pipeList["tcp_data_package_service_pipe"]
        self.FilterGroup.remove_source(ServiceTypes.TCPDPSERVICE)
        try:
            self.TCPDataPackageService.terminate()
        except Exception as e:
            logger.error(
                "there's been an exception in the termination of DataPackage Service "
                + str(e)
            )
            return -1
        try:
            self.TCPDataPackageService.join()
        except Exception as e:
            logger.error(
                "there's been an exception in the joining of DataPackage Service "
                + str(e)
            )
            return -1
        self.tcp_data_package_service_pipe.close()
        return 1

    def start_ssl_data_package_service(self, FTSServiceStartupConfigObject):
        """start SSL DP service and initiate ISC resources

        :param FTSServiceStartupConfigObject:
        :return:
        """
        try:
            print("start 213")
            self.ssl_data_package_service = Queue()
            self.SSLDataPackageService = multiprocessing.Process(
                target=SSLFlaskFunctions().startup,
                args=(
                    FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP,
                    FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort,
                    self.ssl_data_package_service,
                ),
            )
            print("starting SSL now")
            self.SSLDataPackageService.start()
            self.pipeList["ssl_data_package_service"] = self.ssl_data_package_service
            self.FilterGroup.add_source(
                self.ssl_data_package_service, ServiceTypes.SSLDPSERVICE
            )
            time.sleep(2)
            return 1
        except Exception as e:
            logger.error(
                "there has been an exception in the individual starting of the Data Packages Service "
                + str(e)
            )
            return -1

    def stop_ssl_data_package_service(self):
        """stop the SSL DP service and terminate ISC resources

        :return:
        """
        del self.pipeList["ssl_data_package_service"]
        self.FilterGroup.remove_source(ServiceTypes.SSLDPSERVICE)
        try:
            self.SSLDataPackageService.terminate()
        except Exception as e:
            logger.error(
                "there's been an exception in the termination of DataPackage Service "
                + str(e)
            )
            return -1
        try:
            self.SSLDataPackageService.join()
        except Exception as e:
            logger.error(
                "there's been an exception in the joining of DataPackage Service "
                + str(e)
            )
            return -1
        self.ssl_data_package_service.close()
        return 1

    def start_ssl_cot_service(self, FTSServiceStartupConfigObject):
        """start the SSL CoT service and the required ISC resources

        :param FTSServiceStartupConfigObject:
        :return:
        """
        try:
            self.core_ssl_user_queue_send = Queue()
            self.service_ssl_user_queue_send = Queue()
            SSLCoTServicePipeFTS = Queue()
            SSLCoTServicePipeController = Queue()
            self.SSLCoTServicePipe = QueueManager(
                SSLCoTServicePipeFTS, SSLCoTServicePipeController
            )
            SSLCoTServicePipe = QueueManager(
                SSLCoTServicePipeController, SSLCoTServicePipeFTS
            )
            self.SSLCoTPoisonPill = multiprocessing.Event()
            self.SSLCoTPoisonPill.set()
            self.ReceiveConnectionsReset = multiprocessing.Event()
            self.SSLCoTService = multiprocessing.Process(
                target=SSLCoTServiceController().start,
                args=(
                    FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceIP,
                    FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServicePort,
                    self.SSLCoTPoisonPill,
                    self.service_ssl_user_queue_send,
                    self.ReceiveConnectionsReset,
                    SSLCoTServicePipe,
                    self.core_ssl_user_queue_send,
                    ObjectFactory.get_instance("factory"),
                ),
            )
            self.SSLCoTService.start()
            self.pipeList["SSLCoTServiceFTSPipe"] = self.SSLCoTServicePipe
            self.FilterGroup.add_source(
                self.SSLCoTServicePipe, ServiceTypes.SSLCOTSERVICE
            )
            self.FilterGroup.add_receiver(
                self.SSLCoTServicePipe, ServiceTypes.SSLCOTSERVICE
            )
            print("SSL CoTService started")
            return 1
        except Exception as e:
            logger.error(
                "an exception has been thrown in SSL CoT service startup " + str(e)
            )
            return -1

    def stop_ssl_cot_service(self):
        """stop SSL COT service and terminate ISC resources

        :return:
        """
        try:
            self.SSLClientDataPipe.close()
            self.SSLCoTPoisonPill.clear()

            time.sleep(0.1)
            if self.SSLCoTService.is_alive():
                self.SSLCoTService.terminate()
                self.SSLCoTService.join()
            else:
                self.SSLCoTService.join()
            del self.pipeList["SSLCoTServiceFTSPipe"]
            self.FilterGroup.remove_source(ServiceTypes.SSLCOTSERVICE)
            self.FilterGroup.remove_receiver(ServiceTypes.SSLCOTSERVICE)

        except Exception as e:
            logger.error(
                "there's been an exception in the stopping of CoT Service " + str(e)
            )
            return -1
        return 1

    def start_federation_client_service(self, FTSServiceStartupConfigObject):
        """start the federation_client service and the required ISC resources

        :param FTSServiceStartupConfigObject:
        :return:
        """
        FederationClientServicePipeFTS = Queue()
        FederationClientServicePipe = Queue()
        self.FederationClientServicePipeFTS = QueueManager(
            FederationClientServicePipeFTS, FederationClientServicePipe
        )
        FederationClientServicePipe = QueueManager(
            FederationClientServicePipe, FederationClientServicePipeFTS
        )
        self.FederationClientService = multiprocessing.Process(
            target=FederationClientServiceController().start,
            args=(FederationClientServicePipe,),
        )
        self.FederationClientService.start()
        self.pipeList[
            "FederationClientServiceFTSPipe"
        ] = self.FederationClientServicePipeFTS
        self.FilterGroup.add_source(
            self.FederationClientServicePipeFTS, ServiceTypes.FEDCLIENTSERVICE
        )
        self.FilterGroup.add_receiver(
            self.FederationClientServicePipeFTS, ServiceTypes.FEDCLIENTSERVICE
        )
        return 1

    def stop_federation_client_service(self):
        """stop the federation_client service and terminate the ISC resources

        :return:
        """
        try:
            del self.pipeList["FederationClientServiceFTSPipe"]
            if self.FederationClientService.is_alive():
                self.FederationClientService.terminate()
                self.FederationClientService.join()
            else:
                self.FederationClientService.join()

            self.FilterGroup.remove_receiver(ServiceTypes.FEDCLIENTSERVICE)
            self.FilterGroup.remove_source(ServiceTypes.FEDCLIENTSERVICE)
            return 1
        except:
            return -1

    def start_federation_server_service(self, FTSServiceStartupConfigObject):
        """

        :param FTSServiceStartupConfigObject:
        :return:
        """
        try:
            ip = (
                FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceIP
            )
            port = (
                FTSServiceStartupConfigObject.FederationServerService.FederationServerServicePort
            )
            FederationServerServiceFTS = Queue()
            FederationServerServiceController = Queue()
            self.FederationServerServicePipeFTS = QueueManager(
                FederationServerServiceController, FederationServerServiceFTS
            )
            FederationServerServicePipe = QueueManager(
                FederationServerServiceFTS, FederationServerServiceController
            )
            self.FederationServerService = multiprocessing.Process(
                target=FederationServerService().start,
                args=(FederationServerServicePipe, ip, port),
            )
            self.FederationServerService.start()
            self.pipeList[
                "FederationServerServiceFTSPipe"
            ] = self.FederationServerServicePipeFTS
            self.FilterGroup.add_source(
                self.FederationServerServicePipeFTS, ServiceTypes.FEDSERVERSERVICE
            )
            self.FilterGroup.add_receiver(
                self.FederationServerServicePipeFTS, ServiceTypes.FEDSERVERSERVICE
            )
            return 1
        except Exception as e:
            return -1

    def stop_federation_server_service(self):
        try:
            if self.FederationServerService.is_alive():
                self.FederationServerService.terminate()
                self.FederationServerService.join()
            else:
                self.FederationServerService.join()
            self.FederationServerServicePipeFTS.close()
            self.FilterGroup.remove_source(ServiceTypes.FEDSERVERSERVICE)
            self.FilterGroup.remove_receiver(ServiceTypes.FEDSERVERSERVICE)
            return 1
        except:
            return -1

    def register_components(self, FTSServiceStartupConfigObject: FTSObj):
        """this method is responsible for registering all FTS components"""
        # define routing configuration
        self.configuration = InifileConfiguration("")
        self.configuration.add_configuration(
            str(
                pathlib.PurePath(
                    str(config.MainPath),
                    "configuration",
                    "routing",
                    "action_mapping.ini",
                )
            ),
        )

        factory = DefaultFactory(self.configuration)

        ObjectFactory.configure(factory)
        ObjectFactory.register_instance("configuration", self.configuration)

        # register the internal components
        core_components = RegistrationHandler.discover_components(
            component_folder_path=pathlib.PurePath(
                FTSServiceStartupConfigObject.ComponentRegistration.core_components_path
            ),
        )

        for core_component in core_components:
            RegistrationHandler.register_component(
                core_component,
                FTSServiceStartupConfigObject.ComponentRegistration.core_components_import_root,
                self.configuration,
            )

        # register the external components
        external_components = RegistrationHandler.discover_components(
            component_folder_path=pathlib.PurePath(
                FTSServiceStartupConfigObject.ComponentRegistration.external_components_path
            ),
        )

        for external_component in external_components:
            RegistrationHandler.register_component(
                external_component,
                FTSServiceStartupConfigObject.ComponentRegistration.external_components_import_root,
                self.configuration,
            )

        # factory instance is registered for use by the routing worker so that
        # the instances in the instance dictionary can be preserved when the
        # new object factory is instantiated in the sub-process
        ObjectFactory.register_instance("factory", factory)

    def start_routing_proxy_service(self, FTSServiceStartupConfigObject: FTSObj):
        """this function is responsible for starting the routing proxy service"""
        try:
            # define routing configuration

            # define the configuration for the routing worker
            self.configuration.set_value(
                key="server_address",
                value=f"{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxyRequestServerProtocol}://{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxyRequestServerIP}:{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxyRequestServerPort}",
                section="RoutingWorker",
            )

            # define the configuration for the action mapper (the default action mapper is
            # specified as utilization of this service implicitly assumes that the async
            # action mapper is the default action mapper)
            self.configuration.set_value(
                key="routing_publisher_address",
                value=f"{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxyPublisherProtocol}://{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxyPublisherIP}:{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxyPublisherPort}",
                section="ActionMapper",
            )

            self.configuration.set_value(
                key="routing_subscriber_address",
                value=f"{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxySubscriberProtocol}://{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxySubscriberIP}:{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxySubscriberPort}",
                section="ActionMapper",
            )

            # define the configuration for the routing proxy service

            self.configuration.set_value(
                key="frontend_sub_address",
                value=f"{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxySubscriberProtocol}://{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxySubscriberIP}:{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxySubscriberPort}",
                section="RoutingProxy",
            )

            self.configuration.set_value(
                key="frontend_pub_address",
                value=f"{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxyPublisherProtocol}://{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxyPublisherIP}:{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxyPublisherPort}",
                section="RoutingProxy",
            )

            self.configuration.set_value(
                key="backend_address",
                value=f"{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxyRequestServerProtocol}://{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxyRequestServerIP}:{FTSServiceStartupConfigObject.RoutingProxyService.RoutingProxyRequestServerPort}",
                section="RoutingProxy",
            )

            self.configuration.set_value(
                key="worker_count",
                value=int(
                    FTSServiceStartupConfigObject.RoutingProxyService.NumRoutingWorkers
                ),
                section="RoutingProxy",
            )

            # begin the routing proxy
            self.routing_proxy_service = ObjectFactory.get_instance("RoutingProxy")
            proc = multiprocessing.Process(
                target=self.routing_proxy_service.begin_routing
            )
            proc.start()

            return 1

        except Exception as e:
            return -1

    def stop_routing_proxy_service(self):
        """this function is responsible for stopping the routing proxy service"""
        try:
            # TODO: add a pre termination call to shutdown workers and sockets before a
            # termination to prevent hanging resources
            if self.routing_proxy_service.is_alive():
                self.routing_proxy_service.terminate()
                self.routing_proxy_service.join()
            else:
                self.routing_proxy_service.join()
            return 1
        except Exception as e:
            return -1

    # change object name to FTSServiceStartupConfigObject
    def start_all(self, FTSServiceStartupConfigObject):
        import copy

        try:
            if (
                FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus
                == "start"
            ):
                self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus = (
                    FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus
                )
                if (
                    isinstance(self.TCPDataPackageService, multiprocessing.Process)
                    and self.TCPDataPackageService.is_alive()
                ):  # stop the running service and restart, this applies primarily to port changes
                    self.stop_tcp_data_package_service()
                self.start_tcp_data_package_service(FTSServiceStartupConfigObject)
                if (
                    FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort
                    != ""
                ):
                    self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort = (
                        FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort
                    )
                if (
                    FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP
                    != ""
                ):
                    self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP = (
                        FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP
                    )

            elif (
                FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus
                == "stop"
            ):
                self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus = (
                    FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus
                )
                self.stop_tcp_data_package_service()
            else:
                if (
                    FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP
                    != self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP
                    or self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort
                    != FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort
                ):
                    if (
                        FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus
                        == "start"
                        or self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceStatus
                        == "start"
                    ):
                        self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP = (
                            FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP
                        )
                        self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort = (
                            FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServicePort
                        )
                        self.stop_tcp_data_package_service()
                        self.start_tcp_data_package_service(
                            FTSServiceStartupConfigObject
                        )
                    else:
                        self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP = (
                            FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP
                        )

            if (
                FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus
                == "start"
            ):
                self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus = (
                    FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus
                )
                if (
                    isinstance(self.SSLDataPackageService, multiprocessing.Process)
                    and self.SSLDataPackageService.is_alive()
                ):  # stop the running service and restart, this applies primarily to port changes
                    self.stop_ssl_data_package_service()
                self.start_ssl_data_package_service(FTSServiceStartupConfigObject)
                if (
                    FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort
                    != ""
                ):
                    self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort = (
                        FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort
                    )
                if (
                    FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP
                    != ""
                ):
                    self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP = (
                        FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP
                    )
            elif (
                FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus
                == "stop"
            ):
                self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus = (
                    FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus
                )
                self.stop_ssl_data_package_service()
            else:
                if (
                    FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort
                    != ""
                ):
                    self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort = (
                        FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServicePort
                    )
                if (
                    FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP
                    != self.FTSServiceStartupConfigObject.TCPDataPackageService.TCPDataPackageServiceIP
                ):
                    if (
                        FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus
                        or self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceStatus
                    ):
                        self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP = (
                            FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP
                        )
                        self.stop_ssl_data_package_service()
                        self.start_ssl_data_package_service(
                            FTSServiceStartupConfigObject
                        )
                    else:
                        self.FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP = (
                            FTSServiceStartupConfigObject.SSLDataPackageService.SSLDataPackageServiceIP
                        )

            if FTSServiceStartupConfigObject.CoTService.CoTServiceStatus == "start":
                self.FTSServiceStartupConfigObject.CoTService.CoTServiceStatus = (
                    FTSServiceStartupConfigObject.CoTService.CoTServiceStatus
                )
                if (
                    isinstance(self.CoTService, multiprocessing.Process)
                    and self.CoTService.is_alive()
                ):  # stop the running service and restart, this applies primarily to port changes
                    self.stop_cot_service()
                self.start_cot_service(FTSServiceStartupConfigObject)
                if FTSServiceStartupConfigObject.CoTService.CoTServicePort != "":
                    self.FTSServiceStartupConfigObject.CoTService.CoTServicePort = (
                        FTSServiceStartupConfigObject.CoTService.CoTServicePort
                    )
                if FTSServiceStartupConfigObject.CoTService.CoTServiceIP != "":
                    self.FTSServiceStartupConfigObject.CoTService.CoTServiceIP = (
                        FTSServiceStartupConfigObject.CoTService.CoTServiceIP
                    )

            elif FTSServiceStartupConfigObject.CoTService.CoTServiceStatus == "stop":
                self.FTSServiceStartupConfigObject.CoTService.CoTServiceStatus = (
                    FTSServiceStartupConfigObject.CoTService.CoTServiceStatus
                )
                self.stop_cot_service()
            else:
                pass

            if (
                FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceStatus
                == "start"
            ):
                self.FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceStatus = (
                    FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceStatus
                )
                if (
                    isinstance(self.SSLCoTService, multiprocessing.Process)
                    and self.SSLCoTService.is_alive()
                ):  # stop the running service and restart, this applies primarily to port changes
                    self.stop_ssl_cot_service()
                self.start_ssl_cot_service(FTSServiceStartupConfigObject)
                if FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServicePort != "":
                    self.FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServicePort = (
                        FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServicePort
                    )
                if FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceIP != "":
                    self.FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceIP = (
                        FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceIP
                    )

            elif (
                FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceStatus
                == "stop"
            ):
                self.FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceStatus = (
                    FTSServiceStartupConfigObject.SSLCoTService.SSLCoTServiceStatus
                )
                self.stop_ssl_cot_service()

            else:
                pass

            if (
                FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceStatus
                == "start"
            ):
                self.FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceStatus = (
                    FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceStatus
                )
                if (
                    isinstance(self.FederationClientService, multiprocessing.Process)
                    and self.FederationClientService.is_alive()
                ):  # stop the running service and restart, this applies primarily to port changes
                    self.stop_federation_client_service()
                self.start_federation_client_service(FTSServiceStartupConfigObject)
                if (
                    FTSServiceStartupConfigObject.FederationClientService.FederationClientServicePort
                    != ""
                ):
                    self.FTSServiceStartupConfigObject.FederationClientService.FederationClientServicePort = (
                        FTSServiceStartupConfigObject.FederationClientService.FederationClientServicePort
                    )
                if (
                    FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceIP
                    != ""
                ):
                    self.FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceIP = (
                        FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceIP
                    )

            elif (
                FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceStatus
                == "stop"
            ):
                self.FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceStatus = (
                    FTSServiceStartupConfigObject.FederationClientService.FederationClientServiceStatus
                )
                self.stop_federation_client_service()

            else:
                pass

            if (
                FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus
                == "start"
            ):
                self.FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus = (
                    FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus
                )
                if (
                    isinstance(self.FederationServerService, multiprocessing.Process)
                    and self.FederationServerService.is_alive()
                ):  # stop the running service and restart, this applies primarily to port changes
                    self.stop_federation_server_service()
                self.start_federation_server_service(FTSServiceStartupConfigObject)
                if (
                    FTSServiceStartupConfigObject.FederationServerService.FederationServerServicePort
                    != ""
                ):
                    self.FTSServiceStartupConfigObject.FederationServerService.FederationServerServicePort = (
                        FTSServiceStartupConfigObject.FederationServerService.FederationServerServicePort
                    )
                if (
                    FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceIP
                    != ""
                ):
                    self.FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceIP = (
                        FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceIP
                    )

            elif (
                FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus
                == "stop"
                and self.FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus
                != "stop"
            ):
                self.FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus = (
                    FTSServiceStartupConfigObject.FederationServerService.FederationServerServiceStatus
                )
                self.stop_federation_server_service()

            else:
                pass

            return 1
        except Exception as e:
            logger.error("there has been an exception in FTS start_all " + str(e))
            return -1

    def restart_receive_connection_process(self):
        self.ReceiveConnectionsReset.set()
        return 1

    def receive_data_froCoT_service_thread(self, recv_pipe, clientArray, send_pipe):
        """this is the method centrally responsible for the managment of User information
        it receives all client information operations from all services and updates the central
        user_dict accordingl

        Args:
            recv_pipe: the queue to receive client information from
            clientArray:
            send_pipe: the queue to send updates to

        Returns:

        """
        # pip data should be composed of 3 parts, [operation, modelObject, opensockets, connection_object(only necessary for add opp)]
        try:
            # TODO: change 'add' 'remove' 'update' and 'get' to an enumeration
            try:
                data = recv_pipe.get(timeout=config.MainLoopDelay / 1000)
            except queue.Empty:
                return self.user_dict
            if data:
                self.socketCount = data[2]

                if data[0] == "add":
                    # when add is called user is added to the user_dict with a connection object
                    if isinstance(data[1], Presence) and isinstance(
                        data[3], Connection
                    ):
                        user_object = User(m_presence=data[1], connection=data[3])
                        self.user_dict[user_object.user_id] = user_object
                        self.RestAPIPipe.put(data[1])

                    else:
                        logger.error(
                            "error in adding client data to user_dict client presence data: "
                            + str(data[1])
                            + " client connection data: "
                            + str(data[3])
                        )

                elif data[0] == "remove":
                    logger.debug("removing client " + str(data[1].user_id))
                    self.user_dict[data[1].user_id].delete_connection(data[3])
                    if (
                        len(self.user_dict[data[1].user_id].connections) < 1
                    ):  # prevent users connected to more than one service being completely deleted upon disconnect
                        logger.debug(
                            "client " + str(data[1].user_id) + " deleted from user_dict"
                        )
                        del self.user_dict[data[1].user_id]
                    logger.debug("user_dict is now " + str(self.user_dict))

                elif data[0] == "update":
                    # when update is called user object is updated within the user_dict
                    if isinstance(data[1], Presence):
                        self.user_dict[data[1].modelObject.uid].m_presence = data[1]
                    else:
                        logger.error(
                            "error in updating existing client data in user_dict client presence data: "
                            + str(data)
                        )

                elif data[0] == "get":
                    if data[1] == None:
                        send_pipe.put(self.user_dict)
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
            logger.error(
                "exception has been thrown in receive_data_froCoT_service_thread "
                + str(e)
                + " "
                + " error on line: "
                + str(line)
                + "\n user_dict: "
                + str(self.user_dict)
                + "\n data: "
                + str(data)
                + "\n connections "
                + str(self.user_dict[data[1].user_id].connections),
                exc_info=True,
            )
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
                logger.error(
                    "there has been an exception thrown in processing rest command "
                    + str(e)
                )
                self.RestAPICommandsFTS.put("500")

    def check_server_status(self):
        return self.FTSServiceStartupConfigObject

    def help(self):
        print("start_all: to begin all services type")
        print("start_cot_service: to begin CoT service type")
        print("start_data_package_service: to begin data package service  type")
        print("stop_all: to terminate all services type")
        print("stop_cot_service: to terminate CoT service type")
        print("stop_data_package_service: to begin data package service type")
        print("check_service_status: to check the status of the services type")
        print("show_users: to show connected user information type")
        print(
            "start_federation_client_service: to begin federation with another server"
        )
        print("kill: to kill the full server type")

    def show_users(self):
        """
        this method is used only by commands submitted over the rest interface
        """
        data = [["", "", ""]]
        objects = []
        output = []
        print(self.user_dict)
        for client in self.user_dict:
            data.append(
                [
                    client.IP,
                    client.modelObject.detail.contact.callsign,
                    client.modelObject.detail._group.name,
                ]
            )
        for client in data:
            simpleClient = SimpleClient()
            simpleClient.callsign = client[1]
            simpleClient.team = client[2]
            simpleClient.ip = client[0]
            objects.append(simpleClient)

        output.append("total sockets: " + str(self.socketCount))
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
            logger.error(
                "there has been an exception in FTS verifying output " + str(e)
            )
            return False

    def kill(self):
        try:
            self.killSwitch = True
            return 1
        except Exception as e:
            logger.error("error in kill function " + str(e))

    def checkPipes(self):
        """this method is used to check the contents of all pipes sharing data with the core"""
        while True:
            try:
                for service_name, pipe in self.FilterGroup.get_sources().items():
                    try:
                        data = AddDataToCoTList().recv(
                            pipe, timeout=config.MainLoopDelay / 1000
                        )
                    except Exception as e:
                        logger.error("get pipe data failed " + str(e))
                        continue
                    # this runs in the event a new client has connected
                    try:
                        if data == 0 or data is None:
                            continue
                        elif isinstance(data, list):
                            self.data_from_services += len(data)
                            AddDataToCoTList().send(
                                self.FilterGroup.receivers, data[0], service_name
                            )
                            for client in self.user_dict.values():
                                AddDataToCoTList().send(
                                    self.FilterGroup.receivers,
                                    client.m_presence,
                                    service_name,
                                )  # send presence objects of all clients too the service with a new client
                        # this runs in all other cases in which data is received
                        elif data != 0 and data is not None:
                            self.data_from_services += 1
                            AddDataToCoTList().send(
                                self.FilterGroup.receivers, data, service_name
                            )
                        # this runs when a timeout is triggered
                        else:
                            pass
                    except Exception as e:
                        logger.error(
                            "processing received connection data failed " + str(e)
                        )
            except Exception as e:
                logger.error("exception in checking pipes " + str(e))

    def startup(
        self,
        CoTPort,
        CoTIP,
        DataPackagePort,
        DataPackageIP,
        SSLDataPackagePort,
        SSLDataPackageIP,
        RestAPIPort,
        RestAPIIP,
        SSLCoTPort,
        SSLCoTIP,
        AutoStart,
        firstStart=False,
        UI="False",
    ):
        try:
            self.dbController.remove_user()
            self.FTSServiceStartupConfigObject.RestAPIService.RestAPIServiceStatus = (
                "start"
            )
            self.FTSServiceStartupConfigObject.RestAPIService.RestAPIServicePort = (
                RestAPIPort
            )
            self.FTSServiceStartupConfigObject.RestAPIServiceIP = RestAPIIP
            if firstStart:
                from datetime import datetime as dt

                self.StartupTime = dt.now()
            else:
                pass
            if AutoStart == "False":
                StartupObject = FTSObj()
                StartupObject.RestAPIService.RestAPIServicePort = RestAPIPort
                StartupObject.RestAPIService.RestAPIServiceIP = RestAPIIP
                StartupObject.RestAPIService.RestAPIServiceStatus = "start"
                self.start_rest_api_service(StartupObject)

            else:
                StartupObject = FTSObj()
                StartupObject.CoTService.CoTServiceIP = CoTIP
                StartupObject.CoTService.CoTServicePort = CoTPort
                StartupObject.CoTService.CoTServiceStatus = "start"

                StartupObject.TCPDataPackageService.TCPDataPackageServiceIP = (
                    DataPackageIP
                )
                StartupObject.TCPDataPackageService.TCPDataPackageServicePort = (
                    DataPackagePort
                )
                StartupObject.TCPDataPackageService.TCPDataPackageServiceStatus = (
                    "start"
                )

                StartupObject.SSLDataPackageService.SSLDataPackageServiceIP = (
                    SSLDataPackageIP
                )
                StartupObject.SSLDataPackageService.SSLDataPackageServicePort = (
                    SSLDataPackagePort
                )
                StartupObject.SSLDataPackageService.SSLDataPackageServiceStatus = (
                    "start"
                )

                StartupObject.RestAPIService.RestAPIServicePort = RestAPIPort
                StartupObject.RestAPIService.RestAPIServiceIP = RestAPIIP
                StartupObject.RestAPIService.RestAPIServiceStatus = "start"

                StartupObject.FederationClientService.FederationClientServiceStatus = (
                    "start"
                )

                # define routing proxy service variables
                StartupObject.RoutingProxyService.RoutingProxyStatus = "start"

                # StartupObject.FederationServerService.FederationServerServiceStatus = ''

                StartupObject.SSLCoTService.SSLCoTServiceStatus = "start"
                StartupObject.SSLCoTService.SSLCoTServiceIP = SSLCoTIP
                StartupObject.SSLCoTService.SSLCoTServicePort = SSLCoTPort
                self.start_rest_api_service(StartupObject)
                self.register_components(StartupObject)
                self.start_routing_proxy_service(StartupObject)
                self.start_all(StartupObject)

            start_timer = time.time() - 60
            threading.Thread(target=self.checkPipes).start()
            while True:
                try:
                    if time.time() > start_timer + 15:
                        start_timer = time.time()
                        logger.debug(str(self.user_dict))
                        logger.debug(
                            f"number of CoT messages received by services: {str(self.data_from_services)}"
                        )
                        self.data_from_services = 0
                except Exception as e:
                    logger.error(
                        "the periodic debug message has thrown an error " + str(e)
                    )
                try:
                    self.user_dict = self.receive_data_froCoT_service_thread(
                        self.service_tcp_user_queue_send,
                        self.user_dict,
                        self.core_tcp_user_queue_send,
                    )
                except Exception as e:
                    logger.error(
                        "error thrown receiving clients from tcp CoT pipe " + str(e)
                    )
                try:
                    self.user_dict = self.receive_data_froCoT_service_thread(
                        self.service_ssl_user_queue_send,
                        self.user_dict,
                        self.core_ssl_user_queue_send,
                    )
                except Exception as e:
                    logger.error(
                        "error thrown receiving clients from SSL CoT pipe " + str(e)
                    )
        except Exception as e:
            logger.error("exception in the startup of FTS " + str(e))


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

    def close(self):
        self.sender_queue.close()
        self.listener_queue.close()


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
            print("queue full")
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
        print("data gotten from queue " + str(gotten_data))
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
        parser.add_argument(
            "-CoTPort",
            type=int,
            help=OrchestratorConstants().COTPORTDESC,
            default=FTSObj().CoTService.CoTServicePort,
        )
        parser.add_argument(
            "-CoTIP",
            type=str,
            help=OrchestratorConstants().COTIPDESC,
            default=FTSObj().CoTService.CoTServiceIP,
        )
        parser.add_argument(
            "-SSLCoTPort",
            type=int,
            help=OrchestratorConstants().SSLCOTPORTDESC,
            default=FTSObj().SSLCoTService.SSLCoTServicePort,
        )
        parser.add_argument(
            "-SSLCoTIP",
            type=str,
            help=OrchestratorConstants().SSLCOTIPDESC,
            default=FTSObj().SSLCoTService.SSLCoTServiceIP,
        )
        parser.add_argument(
            "-DataPackagePort",
            type=int,
            help=OrchestratorConstants().APIPORTDESC,
            default=FTSObj().TCPDataPackageService.TCPDataPackageServicePort,
        )
        parser.add_argument(
            "-DataPackageIP",
            type=str,
            help=OrchestratorConstants().APIPORTDESC,
            default=FTSObj().TCPDataPackageService.TCPDataPackageServiceIP,
        )
        parser.add_argument(
            "-SSLDataPackagePort",
            type=int,
            help=OrchestratorConstants().APIPORTDESC,
            default=FTSObj().SSLDataPackageService.SSLDataPackageServicePort,
        )
        parser.add_argument(
            "-SSLDataPackageIP",
            type=str,
            help=OrchestratorConstants().APIPORTDESC,
            default=FTSObj().SSLDataPackageService.SSLDataPackageServiceIP,
        )
        parser.add_argument(
            "-RestAPIPort",
            type=int,
            help=OrchestratorConstants().APIPORTDESC,
            default=FTSObj().RestAPIService.RestAPIServicePort,
        )
        parser.add_argument(
            "-RestAPIIP",
            type=str,
            help=OrchestratorConstants().APIPORTDESC,
            default=FTSObj().RestAPIService.RestAPIServiceIP,
        )
        parser.add_argument("-d", type=bool)
        parser.add_argument(
            "-AutoStart",
            type=str,
            help="whether or not you want all services to start or only the root service and the RestAPI service",
            default="True",
        )
        parser.add_argument(
            "-UI",
            type=str,
            help="set to true if you would like to start UI on server startup",
        )
        args = parser.parse_args()
        if config.first_start:
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
        FTS().startup(
            args.CoTPort,
            args.CoTIP,
            args.DataPackagePort,
            args.DataPackageIP,
            args.SSLDataPackagePort,
            args.SSLDataPackageIP,
            args.RestAPIPort,
            args.RestAPIIP,
            args.SSLCoTPort,
            args.SSLCoTIP,
            args.AutoStart,
            True,
            args.UI,
        )
    except Exception as e:
        print(e)
