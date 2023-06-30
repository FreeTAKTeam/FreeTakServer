from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import MissionBase

class Mission(MissionBase):
    __tablename__ = "mission"

    PrimaryKey = Column(String(100), primary_key=True)

    mission_items = relationship("MissionItem", back_populates="mission")

    mission_subscriptions = relationship("Subscription", back_populates="mission")