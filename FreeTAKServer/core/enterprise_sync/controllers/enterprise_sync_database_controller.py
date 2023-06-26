from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject
from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_keyword import EnterpriseSyncKeyword

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
    
    def update_enterprise_sync_data_object(self, filetype: str, objectuid: str, objecthash: str, logger, *args, **kwargs):
        try:
            db_controller = DatabaseController()
            data_obj = db_controller.session.query(EnterpriseSyncDataObject).filter(EnterpriseSyncDataObject.PrimaryKey==objectuid).first()
            data_obj.file_type = filetype
            data_obj.hash = objecthash
            db_controller.session.commit()
        except Exception as ex:
            logger.error("error thrown updating enterprise sync obj: %s err: %s", objectuid, ex)
            db_controller.session.rollback()

    def create_enterprise_sync_data_object(self, filetype: str, objectuid: str, objecthash, obj_length, obj_keywords, obj_start_time, logger, *args, **kwargs):
        """create an enterprise sync data object instance and save it to the database
        with sqlalachemy

        Args:
            filetype (str): the type of the enterprise sync object
            objectuid (str): the uid of the enterprise sync object
        """
        try:
            db_controller = DatabaseController()
            data_obj = EnterpriseSyncDataObject()
            data_obj.file_type = filetype
            data_obj.PrimaryKey = objectuid
            data_obj.hash = objecthash
            data_obj.length = obj_length
            data_obj.start_time = obj_start_time
            
            for obj_keyword in obj_keywords:
                keyword_obj = EnterpriseSyncKeyword()
                keyword_obj.keyword = obj_keyword
                keyword_obj.enterprise_sync_data_object_id = data_obj.PrimaryKey
                db_controller.session.add(keyword_obj)

            db_controller.session.add(data_obj)
            db_controller.session.commit()
        except Exception as ex:
            logger.error("error thrown creating enterprise sync obj: %s err: %s", objectuid, ex)
            db_controller.session.rollback()
            raise ex
            
    def get_enterprise_sync_data_object(self, logger, object_uid: str=None, object_hash: str=None, *args, **kwargs) -> EnterpriseSyncDataObject:
        """retrieve an enterprise sync record based on the object uid

        Args:
            object_uid (str): object uid to be queried
        """
        try:
            db_controller = DatabaseController()
            if object_uid != None:
                data_obj = db_controller.session.query(EnterpriseSyncDataObject).filter(EnterpriseSyncDataObject.PrimaryKey == object_uid).first()
            elif object_hash != None:
                data_obj = db_controller.session.query(EnterpriseSyncDataObject).filter(EnterpriseSyncDataObject.hash == object_hash).first()
            return data_obj
        except Exception as ex:
            logger.error("error thrown getting enterprise sync obj: %s err: %s", object_uid, ex)
            db_controller.session.rollback()
