from sqlalchemy import Column, String, ForeignKey, Boolean, Integer
from sqlalchemy.orm import relationship, composite

from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange

from . import MissionBase
from .mission import Mission

class MissionContent(MissionBase):
    __tablename__ = "mission_content"
    
    PrimaryKey:str = Column(String(1000), primary_key=True) # type: ignore

    mission_uid: str = Column(String(1000), ForeignKey(Mission.PrimaryKey), primary_key=True) # type: ignore

    mission : Mission = relationship(Mission, back_populates="contents")

    change: MissionChange = relationship("MissionChange", back_populates="content_resource")