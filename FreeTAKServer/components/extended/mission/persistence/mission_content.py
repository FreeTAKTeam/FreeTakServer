from sqlalchemy import Column, String, ForeignKey, Boolean, Integer
from sqlalchemy.orm import relationship

from . import MissionBase
from .mission import Mission

class MissionContent(MissionBase):
    __tablename__ = "mission_content"
    
    PrimaryKey:str = Column(String(1000), primary_key=True) # type: ignore

    mission_uid: str = Column(String(1000), ForeignKey(Mission.PrimaryKey)) # type: ignore

    mission : Mission = relationship(Mission, back_populates="contents")