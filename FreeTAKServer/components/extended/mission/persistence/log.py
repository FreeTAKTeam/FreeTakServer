from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .mission_log import MissionLog

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import MissionBase

class Log(MissionBase):
    __tablename__ = "log"
    id: str = Column(String(100), primary_key=True)  # type: ignore
    entryUid: str = Column(String(100))  # type: ignore
    content: str = Column(String)  # type: ignore
    creatorUid: str = Column(String)  # type: ignore
    servertime: str = Column(String)  # type: ignore
    dtg: str = Column(String)  # type: ignore
    created: str = Column(String)  # type: ignore
    
    contentHashes: str = Column(String)  # type: ignore
    
    keywords: str = Column(String)  # type: ignore
    
    missions: List['MissionLog'] = relationship("MissionLog", back_populates="log")
    