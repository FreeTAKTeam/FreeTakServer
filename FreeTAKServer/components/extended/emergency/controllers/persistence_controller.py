from digitalpy.core.persistence.controllers.impl.sqlalchemy_persistence_controller import SQLAlchemyPersistenceController
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.persistence.controllers.persistence_controller import PersistenceController

from ..configuration.emergency_constants import DATABASE_ADDRESS

class PersistenceController(SQLAlchemyPersistenceController):
    def __init__(self,request: Request, response: Response, action_mapper: ActionMapper, configuration: Configuration) -> None:
        super().__init__(request, response, action_mapper, configuration, DATABASE_ADDRESS)
        self.initialize_connection()
    