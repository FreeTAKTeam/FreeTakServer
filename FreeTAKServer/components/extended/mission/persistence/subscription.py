from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import MissionBase
from .mission import Mission

class Subscription(MissionBase):
    __tablename__ = "subscription"

    PrimaryKey = Column(Integer, primary_key=True, autoincrement=True)

    token = Column(String(1000))

    mission_uid = Column(String, ForeignKey(Mission.PrimaryKey))

    mission : Mission = relationship(Mission, back_populates="mission_subscriptions")