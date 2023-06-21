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
from ..persistence.sqlalchemy.excheck_checklist import ExCheckChecklist
from ..persistence.sqlalchemy.excheck_checklist_task import ExCheckChecklistTask
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
        self.ses = self.create_db_session()
        
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
        try:
            template = ExCheckTemplate()
            template.PrimaryKey = templateuid
            self.ses.add(template)
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex

    def create_checklist(self, checklistuid: str, *args, **kwargs):
        """create a checklist db record

        Args:
            checklistuid (str): the uid of the checklist
        """
        try:
            checklist = ExCheckChecklist()
            checklist.PrimaryKey = checklistuid
            self.ses.add(checklist)
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex

    def get_template(self, template_uid: str, *args, **kwargs) -> ExCheckTemplate:
        """
        Retrieve an ExCheckTemplate object from the database based on the template UID.

        Args:
            template_uid (str): The UID of the template to retrieve.

        Returns:
            ExCheckTemplate: The ExCheckTemplate object retrieved from the database.

        """        
        # Query the ExCheckTemplate object based on the template UID
        template = self.ses.query(ExCheckTemplate).filter(ExCheckTemplate.PrimaryKey == template_uid).first()

        return template

    def get_checklist(self, checklist_uid: str, *args, **kwargs) -> ExCheckChecklist:
        """
        Retrieve an ExCheckChecklist object from the database based on the template UID.

        Args:
            checklist_uid (str): The UID of the template to retrieve.

        Returns:
            ExCheckChecklist: The ExCheckChecklist object retrieved from the database.

        """

        # Query the ExCheckChecklist object based on the template UID
        checklist = self.ses.query(ExCheckChecklist).filter(ExCheckChecklist.PrimaryKey == checklist_uid).first()

        return checklist

    def get_checklist_task(self, checklist_task_uid, *args, **kwargs)->ExCheckChecklistTask:
        checklist_task = self.ses.query(ExCheckChecklistTask).filter(ExCheckChecklistTask.PrimaryKey == checklist_task_uid).first()
        return checklist_task

    def get_all_templates(self, *args, **kwargs)->List[ExCheckTemplate]:
        """
        Retrieve all ExCheckTemplate objects from the database.

        Returns:
            ExCheckTemplate: The ExCheckTemplate object retrieved from the database.

        """
        
        # Query the ExCheckTemplate object based on the template UID
        templates = self.ses.query(ExCheckTemplate).all()
                
        return templates
    
    def get_all_checklists(self, *args, **kwargs)->List[ExCheckChecklist]:
        """
        Retrieve all ExCheckTemplate objects from the database.

        Returns:
            ExCheckChecklist: The ExCheckTemplate object retrieved from the database.

        """
        # Query the ExCheckChecklist object based on the template UID
        checklists = self.ses.query(ExCheckChecklist).all()

        return checklists

    def create_template_task(self, templateuid: str, taskuid: str, *args, **kwargs):
        """create a template task db record

        Args:
            templateuid (str): the uid of the parent template of the task
            taskuid (str): the uid of the task itself
        """
        try:
            template_task = ExCheckTemplateTask()
            template_task.PrimaryKey = taskuid
            template_task.template_uid = templateuid
            self.ses.add(template_task)
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex

    def create_checklist_task(self, checklistuid: str, taskuid: str, *args, **kwargs):
        """create a checklist task db record

        Args:
            checklistuid (str): the uid of the parent checklist of the task
            taskuid (str): the uid of the task itself
        """
        try:
            checklist_task = ExCheckChecklistTask()
            checklist_task.PrimaryKey = taskuid
            checklist_task.checklist_uid = checklistuid
            self.ses.add(checklist_task)
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex