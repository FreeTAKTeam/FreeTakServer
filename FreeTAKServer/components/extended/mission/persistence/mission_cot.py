from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange

from .mission import Mission

from . import MissionBase

class MissionCoT(MissionBase):
    __tablename__ = "MissionCoT"
    
    uid = Column(String(100), primary_key=True)
    
    mission_uid: str = Column(String, ForeignKey(Mission.PrimaryKey), primary_key=True) # type: ignore

    mission : Mission = relationship(Mission, back_populates="cots")

    change: MissionChange = relationship("MissionChange", back_populates="cot_detail")