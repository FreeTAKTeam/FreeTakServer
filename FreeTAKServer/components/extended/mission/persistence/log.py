from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import MissionBase

class Log(MissionBase):
    __tablename__ = "mission_log"
    id = Column(String(100), primary_key=True)
    content = Column(String)
    creatorUid = Column(String)
    entryUid = Column(String)
    mission = relationship("MissionLog", back_populates="log")
    servertime = Column(String)
    dtg = Column(String)
    created = Column(String)
    contentHashes = Column(String)
    keywords = Column(String)
    