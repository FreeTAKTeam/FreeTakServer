from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .mission import Mission
from .log import Log

from . import MissionBase

class MissionLog(MissionBase):
    __tablename__ = "mission_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    log_id = Column(String, ForeignKey(Log.id))
    log: Log = relationship(Log, back_populates="mission_logs")
    
    mission_uid = Column(String, ForeignKey(Mission.PrimaryKey))
    mission : Mission = relationship(Mission, back_populates="mission_logs")