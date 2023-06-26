import os
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

config = MainConfig.instance()


WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'

class EnterpriseSyncFormatSynchronizationController(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, sync_action_mapper, configuration)

    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)

    def convert_newlines(self, data: bytes, *args, **kwargs):
        if isinstance(data, str):
            data = data.encode()
            return_str = True
        else:
            return_str = False
        return_data = data.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        if return_str:
            return return_data.decode()
        else:
            return return_data