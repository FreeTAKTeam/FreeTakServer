from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from .mission import Mission

if TYPE_CHECKING:
    pass
    
from . import MissionBase

class MissionToMission(MissionBase):
    __tablename__ = "mission_to_mission"
    
    PrimaryKey: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    
    parent_mission_id: Mapped[str] = Column(String, ForeignKey(Mission.PrimaryKey))
    parent_mission: Mapped['Mission'] = relationship(Mission, back_populates="child_missions", foreign_keys=[parent_mission_id])
    
    child_mission_id: Mapped[str] = Column(String, ForeignKey(Mission.PrimaryKey))
    child_mission: Mapped['Mission'] = relationship(Mission, back_populates="parent_missions", foreign_keys=[child_mission_id])