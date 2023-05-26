import os
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

config = MainConfig.instance()

class EnterpriseSyncFilesystemController(Controller):
    """manage file system operations related to enterprise sync"""

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

    def save_file(self, filetype: str, objectuid: str, objectdata: str, *args, **kwargs):
        """
        Save an enterprise sync file to the file system.

        Args:
            filetype (str): The folder in which the file will be saved.
            objectuid (str): The UID of the file which will be used as the file name.
            objectdata (str): The contents to be saved to the file.
            *args: Additional positional arguments (not used).
            **kwargs: Additional keyword arguments (not used).
        """
        root_path = config.EnterpriseSyncPath
        file_path = os.path.join(root_path, filetype, objectuid + '.txt')
        
        if not os.path.exists(root_path):
            os.mkdir(root_path)

        if not os.path.exists(os.path.join(root_path, filetype)):
            os.mkdir(os.path.join(root_path, filetype))

        with open(file_path, 'wb+') as file:
            file.write(objectdata)
        
    def get_file(self, file_type: str, object_uid: str, *args, **kwargs):
        """
        Retrieve an enterprise sync file from the file system.

        Args:
            iletype (str): The folder in which the file will be saved.
            objectuid (str): The UID of the file which will be used as the file name.
            *args: Additional positional arguments (not used).
            **kwargs: Additional keyword arguments (not used).

        Returns:
            str: The contents of the retrieved file.
        """
        root_path = config.EnterpriseSyncPath
        complete_file_path = os.path.join(root_path, file_type, object_uid+'.txt')

        with open(complete_file_path, 'r') as file:
            file_contents = file.read()

        return file_contents
