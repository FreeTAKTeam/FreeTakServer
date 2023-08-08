from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
import uuid
from sqlalchemy.orm import contains_eager

from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_keyword import EnterpriseSyncKeyword

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
    
    def update_enterprise_sync_object(self, logger, filetype: str=None, objectuid: str=None, objecthash: str=None, obj_length: int=None, obj_keywords: str=None, obj_start_time: str=None, mime_type: str=None, tool: str=None, file_name: str=None, private: int=0, *args, **kwargs):
        try:
            db_controller = DatabaseController()
            data_obj: EnterpriseSyncDataObject = db_controller.session.query(EnterpriseSyncDataObject).filter(EnterpriseSyncDataObject.PrimaryKey==objectuid).first()
            if filetype is not None:
                data_obj.file_type = filetype # type: ignore
            if objecthash is not None:
                data_obj.hash = objecthash # type: ignore
            if obj_length is not None:
                data_obj.length = obj_length # type: ignore
            if obj_keywords is not None:
                data_obj.keywords = obj_keywords # type: ignore
            if obj_start_time is not None:
                data_obj.start_time = obj_start_time # type: ignore
            if mime_type is not None:
                data_obj.mime_type = mime_type # type: ignore
            if tool is not None:
                data_obj.tool = tool # type: ignore
            if file_name is not None:
                data_obj.file_name = file_name # type: ignore
            if private is not None:
                data_obj.private = private # type: ignore
            db_controller.session.commit()
        except Exception as ex:
            logger.error("error thrown updating enterprise sync obj: %s err: %s", objectuid, ex)
            db_controller.session.rollback()

    def create_enterprise_sync_data_object(self, filetype: str, objectuid: str, objecthash, obj_length, obj_keywords, mime_type, tool, file_name, logger, private=0, obj_start_time=None, *args, **kwargs):
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
            if obj_start_time != None:
                data_obj.start_time = obj_start_time
            data_obj.mime_type = mime_type
            data_obj.tool = tool
            data_obj.file_name = file_name
            data_obj.private = private
            
            for obj_keyword in obj_keywords:
                keyword_obj = EnterpriseSyncKeyword()
                keyword_obj.keyword = obj_keyword
                keyword_obj.enterprise_sync_data_object_id = data_obj.PrimaryKey
                data_obj.keywords.append(keyword_obj)
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
            else:
                raise Exception("no object uid or hash provided")
            return data_obj
        except Exception as ex:
            logger.error("error thrown getting enterprise sync obj: %s err: %s", object_uid, ex)
            db_controller.session.rollback()

    def get_all_enterprise_sync_data_objects(self, logger, *args, **kwargs):
        try:
            db_controller = DatabaseController()
            data_objs = db_controller.session.query(EnterpriseSyncDataObject).all()
            return data_objs
        except Exception as ex:
            logger.error("error thrown getting all enterprise sync objs: %s", ex)
            db_controller.session.rollback()

    def get_multiple_enterprise_sync_data_objec(self,  logger, tool: str="*", keyword: str="*", *args, **kwargs):
        try:
            db_controller = DatabaseController()
            data_objs = db_controller.session.query(EnterpriseSyncDataObject)\
            .join(EnterpriseSyncKeyword)\
            .filter(EnterpriseSyncDataObject.tool == tool, EnterpriseSyncKeyword.keyword == keyword).all()
            return data_objs
        except Exception as ex:
            logger.error("error thrown getting enterprise sync objs by tool: %s", ex)
            db_controller.session.rollback()