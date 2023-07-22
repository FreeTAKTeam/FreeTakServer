import pickle
from typing import Dict, List
from FreeTAKServer.core.cot_management.persistence.repeated_message import RepeatedMessage
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.domain.node import Node
from digitalpy.core.digipy_configuration.configuration import Configuration
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, delete

from ..configuration.cot_management_constants import PERSISTENCE_PATH
from ..persistence import CoTManagementBase

class CotManagementRepeaterPersistence(Controller):
    """this class is responsible for persisting repeated messages
    """
    def __init__(self,
        request: Request,
        response: Response,
        cot_management_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, cot_management_action_mapper, configuration)
        self.ses = self.create_db_session()

    def create_db_session(self) -> Session:
        """open a new session in the database

        Returns:
            Session: the session connecting the db
        """
        engine = create_engine(PERSISTENCE_PATH)
        # create a configured "Session" class
        SessionClass = sessionmaker(bind=engine)

        CoTManagementBase.metadata.create_all(engine)

        # create a Session
        return SessionClass()
    
    def create_repeated_message(self, message: Node, id: str) -> RepeatedMessage:
        """create a new repeated message in the database

        Args:
            message (Node): the node object representing the message
            id (str): the id of the node object used to index it
        """
        try:
            repeated_message = RepeatedMessage(id=id, message_contents=message)
            self.ses.add(repeated_message)
            self.ses.commit()
            return repeated_message
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def update_repeated_message(self, message: Node, id: str) -> RepeatedMessage:
        """update a repeated message in the database
        
        Args:
            message (Node): the node object representing the message
            id (str): the id of the node object used to index it
        """
        try:
            repeated_message: RepeatedMessage = self.ses.query(RepeatedMessage).filter(RepeatedMessage.id == id).first() # type: ignore
            repeated_message.message_contents = pickle.dumps(message)
            self.ses.commit()
            return repeated_message
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def delete_repeated_message(self, id: str):
        """remove a repeated message from the database

        Args:
            id (str): the id of the node to be removed
        """
        try:
            delete(RepeatedMessage).where(RepeatedMessage.id == id)
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def get_all_repeated_messages(self) -> List[RepeatedMessage]:
            """get all the repeated messages in the database"""
            return self.ses.query(RepeatedMessage).all()
            
    def get_repeated_message(self, id: str) -> RepeatedMessage:
        """get a repeated message from the database

        Args:
            id (str): the id of the message to be retrieved

        Returns:
            RepeatedMessage: the message object
        """
        return self.ses.query(RepeatedMessage).filter(RepeatedMessage.id == id).first() # type: ignore
            
    def _save_repeated_messages(self, messages: Dict[str, Node]):
        """save a given message to a json file used for persistency in pickled form

        Args:
            message (Dict[str, Node]): entire messages dictionary to be saved
        """
        with open(PERSISTENCE_PATH, "wb+") as f:
            return pickle.dump(messages, f)
        
    def _load_repeated_messages(self)->Dict[str, Node]:
        """load the pickled saved messages asa dictionary

        Returns:
            Dict[str, Node]: a dictionary of message ids and their associated objects
        """
        try:
            with open(PERSISTENCE_PATH, "rb+") as f:
                try:
                    return pickle.load(f)
                # handle the case where the persistence file is empty in which case we simply return an empty dict and save it to the file
                except EOFError:
                    self._save_repeated_messages({})
                    return {}
        except FileNotFoundError:
            # handle the case where the persistence file doesnt exist in which case we simply return an empty dict and save it to the file
            self._save_repeated_messages({})
            return {}