from typing import TYPE_CHECKING, List
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .mission import Mission

if TYPE_CHECKING:
    pass
    
from . import MissionBase

class MissionToMission(MissionBase):
    __tablename__ = "mission_to_mission"
    
    PrimaryKey = Column(Integer, primary_key=True, autoincrement=True)
    
    parent_mission_id = Column(String, ForeignKey(Mission.PrimaryKey))
    parent_mission : Mission = relationship(Mission, back_populates="child_missions", foreign_keys=[parent_mission_id])
    
    child_mission_id = Column(String, ForeignKey(Mission.PrimaryKey))
    child_mission : Mission = relationship(Mission, back_populates="parent_missions", foreign_keys=[child_mission_id])