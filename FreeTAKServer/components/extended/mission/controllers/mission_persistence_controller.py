import codecs
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

    def create_subscription(self, subscription_id, mission_id, *args, **kwargs):
        """this method is used to create a new subscription and save it to the database.
        """
        try:
            subscription = Subscription()
            subscription.PrimaryKey = subscription_id
            subscription.mission_uid = mission_id
            self.ses.add(subscription)
            self.ses.commit()
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

    def create_mission(self, mission_id, mission_data, *args, **kwargs):
        """this method is used to create a new mission, save it to the database and return the mission information
        to the client in json format, it uses the mission persistence controller to access the database.
        """
        try:
            mission = Mission()
            mission.PrimaryKey = mission_id
            mission.MissionData = mission_data
            self.ses.add(mission)
            self.ses.commit()
            return mission
        except Exception as ex:
            self.ses.rollback()
            raise ex
    
    def get_mission(self, mission_id, *args, **kwargs):
        """this method is used to get a mission from the database and return it to the client in json format.
        """
        try:
            mission = self.ses.query(Mission).filter(Mission.PrimaryKey == mission_id).first()
            return mission.MissionData
        except Exception as ex:
            raise ex