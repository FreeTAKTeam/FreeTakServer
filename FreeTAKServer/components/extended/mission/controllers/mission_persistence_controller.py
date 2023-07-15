import codecs
from FreeTAKServer.components.extended.mission.persistence.log import Log

from FreeTAKServer.components.extended.mission.persistence.mission_content import MissionContent
from ..configuration.mission_constants import PERSISTENCE_PATH
from digitalpy.core.main.controller import Controller
import json
import os
import pickle

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from ..persistence.subscription import Subscription
from ..persistence.mission_item import MissionItem
from ..persistence.mission import Mission
from ..persistence import MissionBase
from ..configuration.mission_constants import PERSISTENCE_PATH, DB_PATH

class MissionPersistenceController(Controller):
    """this class is responsible for managing saved components"""

    def __init__(self, request, response, action_mapper, configuration):
        super().__init__(
        request=request,
        response=response,
        action_mapper=action_mapper,
        configuration=configuration,
    )
        super().__init__(request, response, action_mapper, configuration)
        self.ses = self.create_db_session()

    def initialize(self, request, response):
        super().initialize(request, response)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def create_db_session(self) -> Session:
        """open a new session in the database

        Returns:
            Session: the session connecting the db
        """
        engine = create_engine(DB_PATH)
        # create a configured "Session" class
        SessionClass = sessionmaker(bind=engine)

        MissionBase.metadata.create_all(engine)

        # create a Session
        return SessionClass()

    def create_subscription(self, subscription_id, mission_id, token, *args, **kwargs):
        """this method is used to create a new subscription and save it to the database.
        """
        try:
            subscription = Subscription()
            if subscription_id:
                subscription.PrimaryKey = subscription_id
            subscription.mission_uid = mission_id
            subscription.token = token
            self.ses.add(subscription)
            self.ses.commit()
            return subscription
        except Exception as ex:
            self.ses.rollback()
            raise ex

    def get_subscription(self, subscription_id, *args, **kwargs):
        """this method is used to get a subscription from the database.
        """
        try:
            subscription = self.ses.query(Subscription).filter(Subscription.PrimaryKey == subscription_id).first()
            return subscription
        except Exception as ex:
            raise ex

    def create_mission_item(self, mission_id, mission_item_id, mission_item_data, *args, **kwargs):
        """this method is used to create a new mission item and save it to the database.
        """
        try:
            mission_item = MissionItem()
            mission_item.PrimaryKey = mission_item_id
            mission_item.MissionItemData = mission_item_data
            mission_item.mission_uid = mission_id
            self.ses.add(mission_item)
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex

    def get_mission_item(self, mission_item_id, *args, **kwargs):
        """this method is used to get a mission item from the database.
        """
        try:
            mission_item = self.ses.query(MissionItem).filter(MissionItem.PrimaryKey == mission_item_id).first()
            return mission_item
        except Exception as ex:
            raise ex
        
    def create_mission_content(self, mission_id, uid="", hash=""):
        try:
            mission_content = MissionContent()
            mission_content.mission_uid = mission_id
            mission_content.uid = uid # type: ignore
            mission_content.hash = hash # type: ignore
            self.ses.add(mission_content)
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex

    def create_mission(self, mission_id, name, description, uids, contents, createTime, passwordProtected, groups, defaultRole, serviceUri, classification, *args, **kwargs):
        """this method is used to create a new mission, save it to the database and return the mission information
        to the client in json format, it uses the mission persistence controller to access the database.
        """
        try:
            mission = Mission()
            mission.PrimaryKey = mission_id
            mission.name = name
            mission.description = description
            #mission.uids = uids
            mission.contents = contents
            mission.createTime = createTime
            mission.passwordProtected = passwordProtected
            #mission.groups = groups
            mission.defaultRole = defaultRole
            mission.serviceUri = serviceUri
            mission.classification = classification
            self.ses.add(mission)
            self.ses.commit()
            return mission
        except Exception as ex:
            self.ses.rollback()
            raise ex
    
    def get_mission(self, mission_id, *args, **kwargs) -> Mission:
        """this method is used to get a mission from the database and return it to the client in json format.
        """
        try:
            mission: Mission = self.ses.query(Mission).filter(Mission.PrimaryKey == mission_id).first() # type: ignore
            return mission
        except Exception as ex:
            raise ex
        
    def get_all_missions(self, *args, **kwargs):
        try:
            return self.ses.query(Mission).all()
        except Exception as ex:
            raise ex
        
    def create_mission_log(self, id, content, creatorUid, entryUid, mission, servertime, dtg, created, contentHashes, keywords, *args, **kwargs):
        """create a mission log record in the database"""
        try:
            mission_log = Log()
            mission_log.id = id
            mission_log.content = content
            mission_log.creatorUid = creatorUid
            mission_log.entryUid = entryUid
            mission_log.mission = mission
            mission_log.servertime = servertime
            mission_log.dtg = dtg
            mission_log.created = created
            mission_log.contentHashes = contentHashes
            mission_log.keywords = keywords
            self.ses.add(mission_log)
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex