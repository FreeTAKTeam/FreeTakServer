from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from . import MissionBase
from .log import Log
from .mission import Mission

class MissionLog(MissionBase):
    __tablename__ = "mission_log"
    
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    
    log_id: Mapped[str] = Column(String, ForeignKey(Log.id))
    log: Mapped['Log'] = relationship(Log, back_populates="missions")
    
    mission_uid: Mapped[str] = Column(String, ForeignKey(Mission.PrimaryKey))
    mission: Mapped['Mission'] = relationship(Mission, back_populates="logs")