from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject
from FreeTAKServer.core.persistence.DatabaseController import DatabaseController

class EnterpriseSyncDatabaseController(Controller):
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
    
    def create_enterprise_sync_data_object(self, filetype: str, objectuid: str, *args, **kwargs):
        """create an enterprise sync data object instance and save it to the database
        with sqlalachemy

        Args:
            filetype (str): the type of the enterprise sync object
            objectuid (str): the uid of the enterprise sync object
        """
        db_controller = DatabaseController()
        data_obj = EnterpriseSyncDataObject()
        data_obj.file_type = filetype
        data_obj.PrimaryKey = objectuid
        db_controller.session.add(data_obj)
        db_controller.session.commit()
        db_controller.session.close()

    def get_enterprise_sync_data_object(self, object_uid: str) -> EnterpriseSyncDataObject:
        """retrieve an enterprise sync record based on the object uid

        Args:
            object_uid (str): object uid to be queried
        """
        db_controller = DatabaseController()
        data_obj = db_controller.session.query(EnterpriseSyncDataObject).filter(EnterpriseSyncDataObject.PrimaryKey == object_uid).first()
        return data_obj