from sqlalchemy import Column, String, ForeignKey, Boolean, Integer
from sqlalchemy.orm import relationship

from . import MissionBase
from .mission import Mission

class MissionContent(MissionBase):
    __tablename__ = "mission_content"
    
    PrimaryKey = Column(Integer, primary_key=True, autoincrement=True) 
    
    uid = Column(String(100), default="")
    
    hash = Column(String(100), default="")

    mission_uid = Column(String, ForeignKey(Mission.PrimaryKey))

    mission : Mission = relationship(Mission, back_populates="mission_contents")