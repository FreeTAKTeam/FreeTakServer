from datetime import datetime
from lxml import etree
from typing import TYPE_CHECKING
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from FreeTAKServer.core.cot_management.persistence.contact import Contact
from FreeTAKServer.core.cot_management.persistence.dest import Dest
from FreeTAKServer.core.cot_management.persistence.marti import Marti
from FreeTAKServer.core.cot_management.persistence.usericon import Usericon

if TYPE_CHECKING:
    from FreeTAKServer.components.core.domain.domain import Event

from FreeTAKServer.components.core.abstract_component.cot_node import CoTNode
from FreeTAKServer.core.cot_management.persistence import CoTManagementBase
from FreeTAKServer.core.cot_management.persistence.event import Event as DBEvent
from FreeTAKServer.core.cot_management.persistence.point import Point
from FreeTAKServer.core.cot_management.persistence.detail import Detail
from FreeTAKServer.core.domain.node import Node
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from .cot_management_private_cot_controller import CoTManagementPrivateCoTController

from ..configuration.cot_management_constants import (
    BASE_OBJECT,
    BASE_OBJECT_NAME,
)

from ..configuration.cot_management_constants import PERSISTENCE_PATH, DB_PATH

class CoTManagementPersistenceController(Controller):
    """this controller is responsible for general or fundamental component functionality"""
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, sync_action_mapper, configuration)
        self.ses = self.create_db_session()

    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)

    def create_db_session(self) -> Session:
        """open a new session in the database

        Returns:
            Session: the session connecting the db
        """
        engine = create_engine(DB_PATH)
        # create a configured "Session" class
        SessionClass = sessionmaker(bind=engine)

        CoTManagementBase.metadata.create_all(engine)

        # create a Session
        return SessionClass()

    # TODO add logic to update dests
    def update_cot(self, cot_id: str, cot: 'Event'):
        cot_item = self.get_cot(cot_id)
        if cot_item is None:
            raise ValueError("Invalid COT provided.")
        try:
            cot_item.uid = cot.uid
            cot_item.type = cot.type
            cot_item.how = cot.how
            cot_item.time = cot.time
            cot_item.start = cot.start
            cot_item.stale = cot.stale

            cot_item.point.lat = cot.point.lat
            cot_item.point.lon = cot.point.lon
            
            cot_item.detail.xml_content = etree.tostring(cot.detail.xml)

            # 
            if cot_item.detail.contact.uid is None and cot.detail.contact.cot_attributes.values() is not None:
                cot_item.detail.contact = Contact()
            if cot.detail.contact.cot_attributes.values() is not None and cot_item.detail.contact is not None:
                cot_item.detail.contact.callsign = cot.detail.contact.callsign
                cot_item.detail.contact.endpoint = cot.detail.contact.endpoint
                cot_item.detail.contact.iconsetpath = cot.detail.contact.iconsetpath
                cot_item.detail.contact.name = cot.detail.contact.name
                cot_item.detail.contact.emailAddress = cot.detail.contact.emailAddress
                cot_item.detail.contact.xmppUsername = cot.detail.contact.xmppUsername
                cot_item.detail.contact.sipAddress = cot.detail.contact.sipAddress

            if cot_item.detail.usericon is None and cot.detail.usericon.cot_attributes.values() is not None:
                cot_item.detail.usericon = Usericon()

            if cot.detail.usericon.cot_attributes.values() is not None and cot_item.detail.usericon is not None:
                cot_item.detail.usericon.iconsetpath = cot.detail.usericon.iconsetpath
            
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex

    def delete_cot(self, cot_id: str):
        try:
            self.ses.delete(self.get_cot(cot_id))
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def get_cot(self, cot_id: str) -> DBEvent:
        try:
            cot: DBEvent = self.ses.query(DBEvent).filter_by(uid=cot_id).first()
            self.response.set_value("cot", cot)
            return cot
        except Exception as ex:
            raise ex
        
    def create_or_update_cot(self, cot: 'Event'):
        try:
            cot_item = self.get_cot(cot.uid)
            if cot_item is None:
                self.create_cot(cot)
            else:
                self.update_cot(cot.uid, cot)
        except Exception as ex:
            raise ex
        
    def create_cot(self, cot: 'Event'):
        try:
            cot_item = DBEvent()
            cot_item.uid = cot.uid
            cot_item.type = cot.type
            cot_item.how = cot.how
            cot_item.time = cot.time
            cot_item.start = cot.start
            cot_item.stale = cot.stale

            cot_item.point = Point()
            cot_item.point.lat = cot.point.lat
            cot_item.point.lon = cot.point.lon
            
            cot_item.detail = Detail()
            cot_item.detail.xml_content = etree.tostring(cot.detail.xml)
            cot_item.detail.contact = Contact()
            cot_item.detail.contact.callsign = cot.detail.contact.callsign
            cot_item.detail.contact.endpoint = cot.detail.contact.endpoint
            cot_item.detail.contact.iconsetpath = cot.detail.contact.iconsetpath
            cot_item.detail.contact.uid = cot.detail.contact.uid
            cot_item.detail.contact.name = cot.detail.contact.name
            cot_item.detail.contact.emailAddress = cot.detail.contact.emailAddress
            cot_item.detail.contact.xmppUsername = cot.detail.contact.xmppUsername
            cot_item.detail.contact.sipAddress = cot.detail.contact.sipAddress

            cot_item.detail.usericon = Usericon()
            cot_item.detail.usericon.iconsetpath = cot.detail.usericon.iconsetpath
            
            dest_vals = []
            for dest in cot.detail.marti.dest:
                db_dest = Dest()
                dest_vals.append(Dest())
                db_dest.callsign = dest.callsign
            cot_item.detail.marti = Marti()
            cot_item.detail.marti.dest = dest_vals
            self.ses.add(cot_item)
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex