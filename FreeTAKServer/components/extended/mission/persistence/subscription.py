from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import MissionBase
from .mission import Mission

class Subscription(MissionBase):
    __tablename__ = "subscription"

    PrimaryKey = Column(String(100), primary_key=True)

    mission_uid = Column(String, ForeignKey(Mission.PrimaryKey))

    mission = relationship(Mission, back_populates="mission_subscriptions")