from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import MissionBase
from .log import Log
from .mission import Mission

class MissionLog(MissionBase):
    __tablename__ = "mission_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    log_id = Column(String, ForeignKey(Log.id))
    log: Log = relationship(Log, back_populates="missions")
    
    mission_uid = Column(String, ForeignKey(Mission.PrimaryKey))
    mission : Mission = relationship(Mission, back_populates="logs")