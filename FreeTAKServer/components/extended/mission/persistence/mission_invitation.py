from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange
from FreeTAKServer.components.extended.mission.persistence.subscription import Subscription

from .mission import Mission

from . import MissionBase

class MissionInvitation(MissionBase):
    __tablename__ = "MissionInvitation"
    
    uid = Column(String(100), primary_key=True)

    author_uid: str = Column(String, ForeignKey(Mission.PrimaryKey), primary_key=True) # type: ignore
    
    mission_uid: str = Column(String, ForeignKey(Mission.PrimaryKey), primary_key=True) # type: ignore

    subscription: Subscription = relationship("Mission", back_populates="invitation")