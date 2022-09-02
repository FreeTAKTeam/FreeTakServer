import pathlib
from FreeTAKServer.controllers.services.Orchestrator import Orchestrator
from FreeTAKServer.controllers.ClientReceptionHandler import ClientReceptionHandler
from FreeTAKServer.controllers.ReceiveConnections import ReceiveConnections
from FreeTAKServer.controllers.TCPSocketController import TCPSocketController
import os
from digitalpy.core.impl.default_factory import DefaultFactory
from digitalpy.config.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.object_factory import ObjectFactory
from FreeTAKServer.components.core.registration_component.registration_main import (
    Registration,
)
from multiprocessing.pool import ThreadPool
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import (
    DatabaseController,
)

loggingConstants = LoggingConstants(log_name="FTS-TCP_CoT_Service")
logger = CreateLoggerController(
    "FTS-TCP_CoT_Service", logging_constants=loggingConstants
).getLogger()


class TCPCoTServiceController(Orchestrator):
    def component_processed(self, data):
        return 1

    def emergency_received(self, emergency):
        request = ObjectFactory.get_new_instance("request")
        request.set_action("EmergencyReceived")
        request.set_value("emergency", emergency)

        actionmapper = ObjectFactory.get_instance("actionMapper")
        response = ObjectFactory.get_new_instance("response")
        actionmapper.process_action(request, response)

    def start(
        self,
        IP,
        CoTPort,
        Event,
        clientDataPipe,
        ReceiveConnectionKillSwitch,
        RestAPIPipe,
        clientDataRecvPipe,
    ):
        try:
            # define routing
            config = InifileConfiguration("")
            config.add_configuration(
                r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\configuration\routing\action_mapping.ini"
            )

            ObjectFactory.configure(DefaultFactory(config))
            ObjectFactory.register_instance("configuration", config)
            Registration().register_components(
                config,
                component_folder_path=pathlib.Path(
                    pathlib.Path(__file__).parent.parent.parent.absolute(),
                    "components",
                    "core",
                ),
                import_root="FreeTAKServer.components.core",
            )
            Registration().register_components(config)

            self.logger = logger
            self.dbController = DatabaseController()
            # self.clear_user_table()
            os.chdir("../../../")
            # create socket controller
            self.TCPSocketController = TCPSocketController()
            self.TCPSocketController.changeIP(IP)
            self.TCPSocketController.changePort(CoTPort)
            sock = self.TCPSocketController.createSocket()
            pool = ThreadPool(processes=2)
            self.pool = pool
            self.clientDataRecvPipe = clientDataRecvPipe
            clientData = pool.apply_async(
                ClientReceptionHandler().startup, (self.clientInformationQueue,)
            )
            receiveConnection = pool.apply_async(ReceiveConnections().listen, (sock,))
            # instantiate domain model and save process as object
            self.mainRunFunction(
                clientData,
                receiveConnection,
                sock,
                pool,
                Event,
                clientDataPipe,
                ReceiveConnectionKillSwitch,
                RestAPIPipe,
            )
        except Exception as e:
            logger.error(
                "there has been an exception in the start function "
                "of TCPCoTService " + str(e)
            )
            return e
