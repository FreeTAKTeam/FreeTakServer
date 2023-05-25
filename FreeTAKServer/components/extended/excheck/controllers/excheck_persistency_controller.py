from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from typing import List

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from ..persistence.sqlalchemy.excheck_template_task import ExCheckTemplateTask
from ..persistence.sqlalchemy.excheck_template import ExCheckTemplate
from ..persistence.sqlalchemy import ExcheckBase
from ..configuration.excheck_constants import DB_PATH

class ExCheckPersistencyController(Controller):
    """manage the persistency of the excheck controller"""

    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, sync_action_mapper, configuration)

    def create_db_session(self) -> Session:
        """open a new session in the database

        Returns:
            Session: the session connecting the db
        """
        engine = create_engine(DB_PATH)
        # create a configured "Session" class
        SessionClass = sessionmaker(bind=engine)

        ExcheckBase.metadata.create_all(engine)

        # create a Session
        return SessionClass()

    def create_template(self, templateuid: str, *args, **kwargs):
        """create a template db record

        Args:
            templateuid (str): the uid of the template
        """
        ses = self.create_db_session()
        template = ExCheckTemplate()
        template.PrimaryKey = templateuid
        ses.add(template)
        ses.commit()
        ses.close()

    def get_template(self, template_uid: str, *args, **kwargs) -> ExCheckTemplate:
        """
        Retrieve an ExCheckTemplate object from the database based on the template UID.

        Args:
            template_uid (str): The UID of the template to retrieve.

        Returns:
            ExCheckTemplate: The ExCheckTemplate object retrieved from the database.

        """
        ses = self.create_db_session()
        
        # Query the ExCheckTemplate object based on the template UID
        template = ses.query(ExCheckTemplate).filter(ExCheckTemplate.PrimaryKey == template_uid).first()
        
        ses.close()
        
        return template
    
    def get_all_templates(self, *args, **kwargs)->List[ExCheckTemplate]:
        """
        Retrieve all ExCheckTemplate objects from the database.

        Returns:
            ExCheckTemplate: The ExCheckTemplate object retrieved from the database.

        """
        ses = self.create_db_session()
        
        # Query the ExCheckTemplate object based on the template UID
        templates = ses.query(ExCheckTemplate).all()
        
        ses.close()
        
        return templates

    def create_template_task(self, templateuid: str, taskuid: str, *args, **kwargs):
        """create a template task db record

        Args:
            templateuid (str): the uid of the parent template of the task
            taskuid (str): the uid of the task itself
        """
        ses = self.create_db_session()
        template_task = ExCheckTemplateTask()
        template_task.PrimaryKey = taskuid
        template_task.template_uid = templateuid
        ses.add(template_task)
        ses.commit()
        ses.close()